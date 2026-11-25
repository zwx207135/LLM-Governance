"""C-only evidence-use diagnostic; identical retrieved passages, two renderings."""
import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.governance.evidence_binding import EvidenceBindingPolicy, POLICIES
from src.governance.retrieval_scoped import AwardScopedRetrieverV2
from src.utils.experiment_io import RunLedger, sha256_file

RUNTIME = ["experiments/run_c_evidence_binding.py", "src/governance/evidence_binding.py", "src/governance/retrieval_scoped.py",
           "src/governance/retrieval_safe.py", "src/governance/retrieval.py", "src/governance/anti_hallucination.py",
           "src/models/llm_model.py", "src/utils/experiment_io.py"]


def prepare_items(config, data, controls):
    items = [{k: x[k] for k in ("id", "question", "category")} for x in data["items"] if x["id"] in config["existing_ids"]]
    if len(items) != len(config["existing_ids"]):
        raise ValueError("Missing or duplicate selected cases")
    items += config["probes"]
    items += [{"id": x["id"], "question": x["question"], "category": "normal_control"} for x in controls["items"]]
    if len({str(x["id"]) for x in items}) != len(items):
        raise ValueError("Duplicate case identity")
    return items


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    config_path = ROOT / "configs/c_evidence_binding.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    inputs = {"config.json": config_path, **{k + ".json": ROOT / config[k] for k in ("dataset", "controls", "corpus")}}
    data, controls = [json.loads(inputs[k + ".json"].read_text(encoding="utf-8")) for k in ("dataset", "controls")]
    items = prepare_items(config, data, controls)
    modes = list(POLICIES)
    planned = [(str(x["id"]), mode) for i, x in enumerate(items) for mode in modes[i % 2:] + modes[:i % 2]]
    model_path = ROOT / config["model_path"]
    contract = {"config": config, "inputs_sha256": {k: sha256_file(p) for k, p in inputs.items()},
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
    policy = EvidenceBindingPolicy(AwardScopedRetrieverV2(inputs["corpus.json"]), **config["retrieval"])
    pending = ledger.pending(retry_errors=True)
    ledger.manifest.update(status="running", scope="C_method_development_only")
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
            row = {**item, "mode": mode}
            try:
                row.update(policy.prepare(item["question"], mode, item["category"]))
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
