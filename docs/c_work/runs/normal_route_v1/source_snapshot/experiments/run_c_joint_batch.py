"""Configurable, resumable joint integration runs with immutable input/runtime contracts."""
import argparse
import json
import platform
import time
from pathlib import Path
from src.governance.joint_batch import JointBatchService
from src.governance.consistency_v2 import validate_materials
from src.governance.retrieval import LocalRetriever
from src.governance.service import STRATEGIES
from src.utils.experiment_io import RunLedger, sha256_file

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ("experiments/run_c_joint_batch.py", "src/governance/joint_batch.py", "src/governance/joint.py", "src/governance/consistency_v2.py",
           "src/governance/consistency.py", "src/governance/service.py", "src/governance/evidence_policy.py", "src/governance/anti_hallucination.py",
           "src/governance/retrieval.py", "src/models/llm_model.py", "src/utils/experiment_io.py")


def validate(config, items):
    conditions = config["conditions"]
    if not conditions or len({c["name"] for c in conditions}) != len(conditions):
        raise ValueError("Distinct named conditions required")
    if any(c["strategy"] not in STRATEGIES or c["bias_mode"] not in ("off", "prompt") for c in conditions):
        raise ValueError("Batch config supports known C strategies and off/prompt bias modes")
    if type(config["max_new_tokens"]) is not int or not 1 <= config["max_new_tokens"] <= 2048:
        raise ValueError("Invalid token budget")
    if not items or len({str(i["id"]) for i in items}) != len(items):
        raise ValueError("Nonempty unique item IDs required")
    for item in items:
        if not isinstance(item.get("question"), str) or not item["question"].strip():
            raise ValueError("Nonempty question required")
        if set(item) - {"id", "question", "category", "group", "pair_id", "materials"}:
            raise ValueError("No gold/reference fields accepted at this batch boundary")
        validate_materials(item.get("materials", []))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=ROOT / "configs/c_joint_batch.json")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--retry-errors", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--stop-after", type=int)
    args = parser.parse_args()
    if args.stop_after is not None and args.stop_after < 1:
        parser.error("--stop-after must be positive")
    config = json.loads(args.config.read_text(encoding="utf-8"))
    paths = {k: ROOT / config[k] for k in ("dataset", "corpus")}
    items = json.loads(paths["dataset"].read_text(encoding="utf-8"))["items"]
    validate(config, items)
    model_path = ROOT / config["model_path"]
    contract = {"config": config, "dry_run": args.dry_run, "python": platform.python_version(),
                **{k + "_sha256": sha256_file(p) for k, p in paths.items()},
                "runtime_sha256": {p: sha256_file(ROOT / p) for p in RUNTIME},
                "model_sha256": {} if args.dry_run else {p.name: sha256_file(p) for p in model_path.glob("*") if p.suffix in (".json", ".txt", ".safetensors")}}
    conditions = config["conditions"]
    planned = [(str(item["id"]), c["name"]) for index, item in enumerate(items)
               for c in conditions[index % len(conditions):] + conditions[:index % len(conditions)]]
    ledger = RunLedger(args.output, contract, planned, args.resume)
    if not args.resume:
        (args.output / "config.json").write_bytes(args.config.read_bytes())
        for name, p in paths.items():
            (args.output / (name + ".json")).write_bytes(p.read_bytes())
        for name in RUNTIME:
            target = args.output / "source_snapshot" / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes((ROOT / name).read_bytes())
    else:
        for name in paths:
            if sha256_file(args.output / (name + ".json")) != contract[name + "_sha256"]:
                raise ValueError("Stored input changed")
        for name, digest in contract["runtime_sha256"].items():
            if sha256_file(args.output / "source_snapshot" / name) != digest:
                raise ValueError("Stored runtime snapshot changed")
    pending = ledger.pending(args.retry_errors)
    ledger.manifest["status"] = "running"
    ledger.save()
    try:
        model = None
        if pending and not args.dry_run:
            import torch
            import transformers
            from transformers import set_seed
            from src.models.llm_model import LLMModel
            set_seed(config["seed"])
            model = LLMModel(str(model_path), local_files_only=True)
            model.generate("你好", max_new_tokens=8, do_sample=False)
            ledger.manifest.update(device=model.device, torch=torch.__version__, transformers=transformers.__version__, warmup_calls=1)
        service = JointBatchService(LocalRetriever(paths["corpus"]), lambda: model)
        by_id = {str(i["id"]): i for i in items}
        modes = {c["name"]: c for c in conditions}
        for index, (ident, mode) in enumerate(pending, 1):
            item, c = by_id[ident], modes[mode]
            if args.dry_run:
                row = {"status": "prepared", "answer": None, "model_calls": 0, "answer_origin": "dry_run"}
            else:
                set_seed(config["seed"])
                if torch.cuda.is_available():
                    torch.cuda.synchronize()
                start = time.perf_counter()
                row = service.answer(item["question"], c["strategy"], item.get("category"), c["bias_mode"], config["max_new_tokens"], item.get("materials", []))
                if torch.cuda.is_available():
                    torch.cuda.synchronize()
                row["request_seconds"] = time.perf_counter() - start
            row.update(id=item["id"], mode=mode, group=item.get("group", "unspecified"), pair_id=item.get("pair_id"), question=item["question"])
            ledger.append(row)
            print(f"{index}/{len(pending)} {ident} {mode} {row['status']}", flush=True)
            if args.stop_after and index >= args.stop_after and index < len(pending):
                ledger.manifest["status"] = "interrupted"
                ledger.save()
                return
        ledger.manifest["status"] = "completed_with_errors" if ledger.manifest["counts"]["errors"] else "completed"
        ledger.save()
        if ledger.manifest["counts"]["errors"]:
            raise SystemExit(1)
    except BaseException:
        if ledger.manifest["status"] == "running":
            ledger.manifest["status"] = "interrupted"
            ledger.save()
        raise


if __name__ == "__main__":
    main()
