"""Frozen three-policy development comparison, including 20 normal task controls."""
import argparse
import json
import platform
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.governance.evidence_policy import EvidencePolicy, POLICIES
from src.governance.retrieval import LocalRetriever
from src.utils.experiment_io import RunLedger, sha256_file

RUNTIME = ["experiments/run_c_policy_comparison.py", "src/governance/evidence_policy.py",
           "src/governance/anti_hallucination.py", "src/governance/retrieval.py",
           "src/utils/experiment_io.py", "src/models/llm_model.py"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=ROOT / "configs/c_policy_comparison.json")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    config = json.loads(args.config.read_text(encoding="utf-8"))
    if set(config["policies"]) != set(POLICIES) or len(config["policies"]) != len(POLICIES):
        raise ValueError("Comparison requires the frozen three distinct policies")
    dataset_path, controls_path, corpus_path = [ROOT / config[k] for k in ("dataset", "controls", "corpus")]
    dataset = json.loads(dataset_path.read_text(encoding="utf-8"))
    selected = {str(i) for i in config["development_ids"]}
    items = [x for x in dataset["items"] if str(x["id"]) in selected]
    if len(items) != len(selected):
        raise ValueError("Missing or duplicate selected IDs")
    items += [{**x, "data_role": "normal_control"} for x in json.loads(controls_path.read_text(encoding="utf-8"))["items"]]
    if len({str(x["id"]) for x in items}) != len(items):
        raise ValueError("Duplicate sample IDs")
    policies = config["policies"]
    planned = [(str(item["id"]), p) for index, item in enumerate(items)
               for p in policies[index % len(policies):] + policies[:index % len(policies)]]
    model_path = ROOT / config["model_path"]
    contract = {"config": config, "dry_run": args.dry_run,
                "dataset_sha256": sha256_file(dataset_path), "controls_sha256": sha256_file(controls_path),
                "corpus_sha256": sha256_file(corpus_path), "runtime_sha256": {p: sha256_file(ROOT / p) for p in RUNTIME},
                "python": platform.python_version(),
                "model_sha256": {} if args.dry_run else {p.name: sha256_file(p) for p in model_path.glob("*") if p.suffix in (".json", ".txt", ".safetensors")}}
    ledger = RunLedger(args.output, contract, planned, resume=args.resume)
    if not args.resume:
        for name, path in [("config.json", args.config), ("dataset.json", dataset_path), ("controls.json", controls_path), ("corpus.json", corpus_path)]:
            (args.output / name).write_bytes(path.read_bytes())
        for relative in RUNTIME:
            target = args.output / "source_snapshot" / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes((ROOT / relative).read_bytes())
        ledger.manifest["started_at"] = datetime.now(timezone.utc).isoformat()
    else:
        for name, key in [("dataset.json", "dataset_sha256"), ("controls.json", "controls_sha256"), ("corpus.json", "corpus_sha256")]:
            if sha256_file(args.output / name) != contract[key]:
                raise ValueError("Stored input snapshot changed")
    policy = EvidencePolicy(LocalRetriever(corpus_path), **config["retrieval"])
    pending = ledger.pending(retry_errors=True)
    by_id = {str(i["id"]): i for i in items}
    ledger.manifest["status"] = "running"
    ledger.save()
    model = None
    try:
        if not args.dry_run and pending:
            import torch
            import transformers
            from transformers import set_seed
            from src.models.llm_model import LLMModel
            set_seed(config["seed"])
            model = LLMModel(str(model_path), local_files_only=True)
            model.generate("你好", max_new_tokens=8, do_sample=False)
            if torch.cuda.is_available():
                torch.cuda.synchronize()
            ledger.manifest.update(torch=torch.__version__, transformers=transformers.__version__, device=model.device)
        for index, (ident, name) in enumerate(pending, 1):
            item = by_id[ident]
            row = {"id": item["id"], "category": item["category"], "data_role": item.get("data_role", "provisional_reference"),
                   "mode": name, "question": item["question"], "evaluation_status": "pending_independent_review"}
            try:
                start = time.perf_counter()
                prepared = policy.prepare(item["question"], name, item["category"])
                row.update(prepared)
                row["prepare_seconds"] = time.perf_counter() - start
                row.update(answer=None, generation_seconds=0, output_tokens=0, input_tokens=0, truncated=False,
                           model_calls=0, answer_origin="dry_run" if args.dry_run else "model")
                if not args.dry_run:
                    if prepared["answer_override"] is not None:
                        row.update(answer=prepared["answer_override"], answer_origin="policy_abstention")
                    else:
                        set_seed(config["seed"])
                        if torch.cuda.is_available():
                            torch.cuda.synchronize()
                        start = time.perf_counter()
                        row["answer"] = model.generate(prepared["prompt"], **config["generation"])
                        if torch.cuda.is_available():
                            torch.cuda.synchronize()
                        row["generation_seconds"] = time.perf_counter() - start
                        row.update(model.last_generation, model_calls=1)
                    row["answer_characters"] = len(row["answer"])
                row["status"] = "prepared" if args.dry_run else "ok"
            except Exception as exc:
                row.update(status="error", error=f"{type(exc).__name__}: {exc}")
            ledger.append(row)
            print(f"{index}/{len(pending)} {ident} {name} {row['status']} {row.get('answer_origin')}", flush=True)
        ledger.manifest.update(status="completed_with_errors" if ledger.manifest["counts"]["errors"] else "completed",
                               finished_at=datetime.now(timezone.utc).isoformat())
        ledger.save()
        if ledger.manifest["counts"]["errors"]:
            raise SystemExit(1)
    except BaseException as exc:
        if ledger.manifest["status"] == "running":
            ledger.manifest.update(status="interrupted" if isinstance(exc, KeyboardInterrupt) else "failed", error=str(exc))
            ledger.save()
        raise


if __name__ == "__main__":
    main()
