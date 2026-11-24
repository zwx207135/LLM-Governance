"""Paired old/safe retrieval diagnostic: identical corpus, constraints and decoding."""
import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.governance.anti_hallucination import AntiHallucination
from src.governance.retrieval import LocalRetriever
from src.governance.retrieval_safe import SafeAnchorRetriever
from src.utils.experiment_io import RunLedger, sha256_file

RUNTIME = ["experiments/run_c_anchor_diagnostics.py", "src/governance/retrieval_safe.py",
           "src/governance/retrieval.py", "src/governance/anti_hallucination.py",
           "src/models/llm_model.py", "src/utils/experiment_io.py"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    config_path = ROOT / "configs/c_anchor_diagnostics.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    data_path, corpus_path = [ROOT / config[k] for k in ("dataset", "corpus")]
    data = json.loads(data_path.read_text(encoding="utf-8"))
    # Only question, category and identity cross the generation boundary.
    items = [{k: x[k] for k in ("id", "question", "category")} for x in data["items"] if x["id"] in config["existing_ids"]]
    if len(items) != len(config["existing_ids"]):
        raise ValueError("Selected item missing or duplicated")
    items += config["probes"]
    modes = ["legacy", "safe_anchor"]
    planned = [(str(x["id"]), mode) for i, x in enumerate(items) for mode in modes[i % 2:] + modes[:i % 2]]
    model_path = ROOT / config["model_path"]
    contract = {"config": config, "dataset_sha256": sha256_file(data_path), "corpus_sha256": sha256_file(corpus_path),
                "runtime_sha256": {p: sha256_file(ROOT / p) for p in RUNTIME},
                "model_sha256": {p.name: sha256_file(p) for p in model_path.glob("*") if p.suffix in (".json", ".txt", ".safetensors")}}
    ledger = RunLedger(args.output, contract, planned, resume=args.resume)
    snapshots = {"config.json": config_path, "dataset.json": data_path, "corpus.json": corpus_path,
                 **{"source_snapshot/" + p: ROOT / p for p in RUNTIME}}
    for name, source in snapshots.items():
        target = args.output / name
        if args.resume:
            if sha256_file(target) != sha256_file(source):
                raise ValueError("Snapshot changed: " + name)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(source.read_bytes())
    retrievers = {"legacy": LocalRetriever(corpus_path), "safe_anchor": SafeAnchorRetriever(corpus_path)}
    gov = {name: AntiHallucination(r, **config["retrieval"]) for name, r in retrievers.items()}
    pending = ledger.pending(retry_errors=True)
    ledger.manifest.update(status="running", evaluation_status="pending_independent_review")
    ledger.save()
    try:
        import torch
        import transformers
        from transformers import set_seed
        from src.models.llm_model import LLMModel
        set_seed(config["seed"])
        model = LLMModel(str(model_path), local_files_only=True) if pending else None
        ledger.manifest.update(torch=torch.__version__, transformers=transformers.__version__, device=model.device if model else None)
        by_id = {str(x["id"]): x for x in items}
        for i, (ident, mode) in enumerate(pending, 1):
            item = by_id[ident]
            row = {**item, "mode": mode, "evaluation_status": "pending_independent_review"}
            try:
                prepared = gov[mode].prepare(item["question"], "combined", item["category"])
                row.update(prepared)
                row["mode"] = mode
                row["rejected"] = retrievers["safe_anchor"].search_with_diagnostics(item["question"], **config["retrieval"])["rejected"] if mode == "safe_anchor" else []
                set_seed(config["seed"])
                row.update(answer=model.generate(row["prompt"], **config["generation"]), **model.last_generation,
                           status="ok", model_calls=1, answer_origin="model")
            except Exception as exc:
                row.update(status="error", error=f"{type(exc).__name__}: {exc}")
            ledger.append(row)
            print(f"{i}/{len(pending)} {ident} {mode} {row['status']}", flush=True)
        ledger.manifest.update(status="completed_with_errors" if ledger.manifest["counts"]["errors"] else "completed",
                               finished_at=datetime.now(timezone.utc).isoformat())
        ledger.save()
        if ledger.manifest["counts"]["errors"]:
            raise SystemExit(1)
    except BaseException as exc:
        if ledger.manifest["status"] == "running":
            ledger.manifest.update(status="failed", error=str(exc))
            ledger.save()
        raise


if __name__ == "__main__":
    main()
