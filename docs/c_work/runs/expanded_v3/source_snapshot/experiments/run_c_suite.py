"""Resumable paired development runs with frozen inputs and explicit uncertainty probes."""
import argparse
import json
import platform
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.governance.anti_hallucination import AntiHallucination, MODES
from src.governance.retrieval import LocalRetriever
from src.utils.experiment_io import RunLedger, atomic_json, sha256_file

RUNTIME_FILES = ["experiments/run_c_suite.py", "src/utils/experiment_io.py", "src/governance/retrieval.py",
                 "src/governance/anti_hallucination.py", "src/models/llm_model.py"]


def now():
    return datetime.now(timezone.utc).isoformat()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--retry-errors", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--stop-after", type=int, help="Stop cleanly after this segment's N records; resume later")
    args = parser.parse_args()
    if args.retry_errors and not args.resume:
        parser.error("--retry-errors requires --resume")
    if args.stop_after is not None and args.stop_after < 1:
        parser.error("--stop-after must be positive")
    config_path = args.config or (args.output / "config.json" if args.resume else ROOT / "configs/c_expanded.json")
    config = json.loads(config_path.read_text(encoding="utf-8"))
    modes = config["modes"]
    if not modes or len(modes) != len(set(modes)) or any(m not in MODES for m in modes):
        raise ValueError("Invalid or duplicate modes")
    ids = config["development_ids"]
    if not ids or len(set(map(str, ids))) != len(ids):
        raise ValueError("Nonempty unique development IDs required")
    dataset_path, corpus_path = ROOT / config["dataset"], ROOT / config["corpus"]
    dataset = json.loads(dataset_path.read_text(encoding="utf-8"))
    by_id = {str(r["id"]): r for r in dataset["items"]}
    if len(by_id) != len(dataset["items"]) or any(str(i) not in by_id for i in ids):
        raise ValueError("Duplicate or missing dataset IDs")
    items = [by_id[str(i)] for i in ids]
    # Rotate mode order by sample to reduce a fixed warm-cache/thermal order effect.
    planned = []
    for index, item in enumerate(items):
        shift = index % len(modes)
        planned.extend((str(item["id"]), m) for m in modes[shift:] + modes[:shift])
    model_path = ROOT / config["model_path"]
    model_files = sorted(p for p in model_path.glob("*") if p.suffix in (".json", ".txt", ".safetensors"))
    contract = {"config": config, "dry_run": args.dry_run,
                "dataset_sha256": sha256_file(dataset_path), "corpus_sha256": sha256_file(corpus_path),
                "runtime_sha256": {p: sha256_file(ROOT / p) for p in RUNTIME_FILES},
                "model_sha256": {} if args.dry_run else {p.name: sha256_file(p) for p in model_files}}
    ledger = RunLedger(args.output, contract, planned, resume=args.resume)
    if not args.resume:
        for name, source in [("config.json", config_path), ("dataset.json", dataset_path), ("corpus.json", corpus_path)]:
            (args.output / name).write_bytes(source.read_bytes())
        for folder in (ROOT / "src", ROOT / "experiments"):
            for source in folder.rglob("*.py"):
                target = args.output / "source_snapshot" / source.relative_to(ROOT)
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(source.read_bytes())
        try:
            revision = subprocess.check_output(["git", "-c", f"safe.directory={ROOT.as_posix()}", "-C", str(ROOT), "rev-parse", "HEAD"], text=True).strip()
        except (OSError, subprocess.CalledProcessError):
            revision = None
        ledger.manifest.update(started_at=now(), revision=revision)
    else:
        for filename, expected in [("dataset.json", contract["dataset_sha256"]), ("corpus.json", contract["corpus_sha256"])]:
            if sha256_file(args.output / filename) != expected:
                raise ValueError("Stored input snapshot was modified")
    pending = ledger.pending(args.retry_errors)
    if not pending:
        ledger.manifest["status"] = "completed_with_errors" if ledger.manifest["counts"]["errors"] else "completed"
        ledger.save()
        print(json.dumps(ledger.manifest["counts"]))
        return
    segment = {"started_at": now(), "python": platform.python_version(), "resume": args.resume}
    ledger.manifest["segments"].append(segment)
    ledger.manifest["status"] = "running"
    ledger.save()
    governance = AntiHallucination(LocalRetriever(corpus_path), **config["retrieval"])
    model = None
    torch = None
    try:
        if not args.dry_run:
            import torch
            import transformers
            from transformers import set_seed
            from src.models.llm_model import LLMModel
            set_seed(config["seed"])
            start = time.perf_counter()
            model = LLMModel(str(model_path), local_files_only=True)
            if torch.cuda.is_available():
                torch.cuda.synchronize()
            segment.update(model_load_seconds=time.perf_counter() - start, torch=torch.__version__,
                           transformers=transformers.__version__, device=model.device)
            model.generate("你好", max_new_tokens=8, do_sample=False)
            if torch.cuda.is_available():
                torch.cuda.synchronize()
            ledger.save()
        for number, (ident, mode) in enumerate(pending, 1):
            item = by_id[ident]
            row = {"id": item["id"], "mode": mode, "question": item["question"], "category": item["category"],
                   "data_role": item.get("data_role", "normal_control" if item["category"] == "normal_control" else "provisional_reference"),
                   "evaluation_status": "pending_independent_review"}
            try:
                start = time.perf_counter()
                row.update(governance.prepare(item["question"], mode, item["category"]))
                row["prepare_seconds"] = round(time.perf_counter() - start, 6)
                row["answer"] = None
                if model is not None:
                    set_seed(config["seed"])
                    if torch.cuda.is_available():
                        torch.cuda.synchronize()
                    start = time.perf_counter()
                    row["answer"] = model.generate(row["prompt"], **config["generation"])
                    if torch.cuda.is_available():
                        torch.cuda.synchronize()
                    row["generation_seconds"] = round(time.perf_counter() - start, 6)
                    row.update(model.last_generation)
                row["status"] = "prepared" if args.dry_run else "ok"
            except Exception as exc:
                row.update(status="error", error=f"{type(exc).__name__}: {exc}")
            ledger.append(row)
            print(f"{number}/{len(pending)} {ident} {mode} {row['status']}", flush=True)
            if args.stop_after and number >= args.stop_after and number < len(pending):
                ledger.manifest["status"] = "interrupted"
                segment["finished_at"] = now()
                ledger.save()
                return
        segment["finished_at"] = now()
        ledger.manifest.update(status="completed_with_errors" if ledger.manifest["counts"]["errors"] else "completed", finished_at=now())
        ledger.save()
        if ledger.manifest["counts"]["errors"]:
            raise SystemExit(1)
    except BaseException as exc:
        if ledger.manifest["status"] == "running":
            ledger.manifest.update(status="interrupted" if isinstance(exc, KeyboardInterrupt) else "failed", error=str(exc))
            segment["finished_at"] = now()
            ledger.save()
        raise


if __name__ == "__main__":
    main()
