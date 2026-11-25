"""Verify read-only screening and actual joint smoke outputs without effectiveness claims."""
import json
from pathlib import Path
from src.governance.consistency import check_consistency
from src.utils.experiment_io import sha256_file

ROOT = Path(__file__).resolve().parents[1]


def verify():
    folder = ROOT / "docs/c_work"
    audit = json.loads((folder / "consistency_audit_v1/checks.json").read_text(encoding="utf-8"))
    for name, digest in audit["summary"]["input_sha256"].items():
        if sha256_file(folder / "runs" / name / "records.jsonl") != digest:
            raise ValueError("Audited historical log changed")
    assert len(audit["records"]) == 989
    assert all(r["factual_accuracy"] is None and r["semantic_support"] == "not_evaluated" for r in audit["records"])
    run = folder / "runs/joint_smoke_v1"
    manifest = json.loads((run / "joint_manifest.json").read_text(encoding="utf-8"))
    for name, digest in manifest["runtime_sha256"].items():
        if sha256_file(run / "source_snapshot" / name) != digest:
            raise ValueError("Joint smoke source snapshot changed")
    rows = [json.loads(line) for line in (run / "records.jsonl").read_text(encoding="utf-8").splitlines()]
    assert len(rows) == 6 and len({(r["id"], r["bias_mode"]) for r in rows}) == 6
    for row in rows:
        assert row["status"] == "ok" and row["model_calls"] == 1 and row["answer_origin"] == "model"
        assert row["consistency"] == check_consistency(row["answer"], row["evidence"], row["evidence_labels"])
    result = {"historical_records_audited": 989, "flagged_records_not_errors": audit["summary"]["flagged_records"],
              "joint_model_smoke_outputs": 6, "errors": 0, "semantic_support": "not_evaluated",
              "bias_effectiveness": "not_evaluated", "historical_logs_unchanged": True}
    (folder / "integration_check.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return result


if __name__ == "__main__":
    print(json.dumps(verify(), ensure_ascii=False, indent=2))
