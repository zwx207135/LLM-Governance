"""Verify demonstration snapshots and actual output provenance without grading answers."""
import json
from pathlib import Path

from src.utils.experiment_io import latest_records, read_records, sha256_file, stable_hash

ROOT = Path(__file__).resolve().parents[1]


def main():
    run = ROOT / "docs/c_work/runs/demo_v1"
    manifest = json.loads((run / "manifest.json").read_text(encoding="utf-8"))
    contract = manifest["contract"]
    assert stable_hash(contract) == manifest["contract_sha256"]
    assert manifest["status"] == "completed" and manifest["stage"] == "demonstration_not_evaluation"
    assert sha256_file(run / "corpus.json") == contract["corpus_sha256"]
    for name, expected in contract["runtime_sha256"].items():
        assert sha256_file(run / "source_snapshot" / name) == expected
    rows = latest_records(read_records(run / "records.jsonl"))
    assert set(rows) == set(map(tuple, manifest["planned_records"]))
    assert all(r["status"] == "ok" for r in rows.values())
    assert len(rows) == 12
    program = [r for r in rows.values() if r["answer_origin"] == "policy_abstention"]
    model = [r for r in rows.values() if r["answer_origin"] == "model"]
    assert len(program) == 1 and len(model) == 11
    assert all(r["model_calls"] == 0 and r["output_tokens"] == 0 for r in program)
    assert all(r["model_calls"] == 1 and r["output_tokens"] > 0 for r in model)
    assert all(not set(i) - {"id", "question", "category"} for i in contract["items"])
    result = {"stage": "demonstration_not_evaluation", "records": len(rows), "model_generated_answers": len(model),
              "program_abstentions": len(program), "input_and_runtime_snapshots_verified": True,
              "reference_and_scoring_fields_in_inputs": False, "independent_human_reviews_completed": 0}
    (ROOT / "docs/c_work/demo_verification.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
