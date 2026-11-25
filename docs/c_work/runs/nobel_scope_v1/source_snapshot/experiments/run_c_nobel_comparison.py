"""Isolate corpus expansion from metadata-aware retrieval with real local generation."""
import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.governance.anti_hallucination import AntiHallucination
from src.governance.retrieval_safe import SafeAnchorRetriever
from src.governance.retrieval_scoped import AwardScopedRetriever
from src.utils.experiment_io import RunLedger, sha256_file

RUNTIME = ["experiments/run_c_nobel_comparison.py", "src/governance/retrieval_scoped.py", "src/governance/retrieval_safe.py",
           "src/governance/retrieval.py", "src/governance/anti_hallucination.py", "src/models/llm_model.py", "src/utils/experiment_io.py"]


def prepare_items(config, data):
    items = [{k: x[k] for k in ("id", "question", "category")} for x in data["items"] if x["id"] in config["existing_ids"]]
    if len(items) != len(config["existing_ids"]):
        raise ValueError("Selected item missing or duplicated")
    items += config["probes"]
    if len({str(x["id"]) for x in items}) != len(items):
        raise ValueError("Duplicate sample identity")
    return items


def make_retrievers(corpora):
    return {name: (AwardScopedRetriever if name == "v4_scoped" else SafeAnchorRetriever)(path) for name, path in corpora.items()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    config_path = ROOT / "configs/c_nobel_comparison.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    data_path = ROOT / config["dataset"]
    corpora = {name: ROOT / path for name, path in config["corpora"].items()}
    items = prepare_items(config, json.loads(data_path.read_text(encoding="utf-8")))
    modes = list(corpora)
    planned = [(str(x["id"]), mode) for i, x in enumerate(items) for mode in modes[i % 3:] + modes[:i % 3]]
    model_path = ROOT / config["model_path"]
    inputs = {"dataset.json": data_path, "config.json": config_path, "documents.json": ROOT / config["documents"],
              **{name + "_corpus.json": path for name, path in corpora.items()}}
    contract = {"config": config, "inputs_sha256": {name: sha256_file(path) for name, path in inputs.items()},
                "runtime_sha256": {p: sha256_file(ROOT / p) for p in RUNTIME},
                "model_sha256": {p.name: sha256_file(p) for p in model_path.glob("*") if p.suffix in (".json", ".txt", ".safetensors")}}
    ledger = RunLedger(args.output, contract, planned, resume=args.resume)
    for name, source in {**inputs, **{"source_snapshot/" + p: ROOT / p for p in RUNTIME}}.items():
        target = args.output / name
        if args.resume:
            if sha256_file(target) != sha256_file(source):
                raise ValueError("Snapshot changed: " + name)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(source.read_bytes())
    retrievers = make_retrievers(corpora)
    gov = {name: AntiHallucination(retriever, **config["retrieval"]) for name, retriever in retrievers.items()}
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
                row.update(gov[mode].prepare(item["question"], "combined", item["category"]))
                row["mode"] = mode
                diagnostics = retrievers[mode].search_with_diagnostics(item["question"], **config["retrieval"])
                row.update(rejected=diagnostics["rejected"], selection_events=diagnostics.get("selection_events", []))
                set_seed(config["seed"])
                answer = model.generate(row["prompt"], **config["generation"])
                row.update(answer=answer, **model.last_generation, status="ok", model_calls=1, answer_origin="model")
            except Exception as exc:
                row.update(status="error", error=f"{type(exc).__name__}: {exc}")
            ledger.append(row)
            print(f"{i}/{len(pending)} {ident} {mode} {row['status']}", flush=True)
        ledger.manifest.update(status="completed_with_errors" if ledger.manifest["counts"]["errors"] else "completed", finished_at=datetime.now(timezone.utc).isoformat())
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
