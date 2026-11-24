"""Verify candidate run provenance, raw identities and review packet integrity."""
import csv
import json
from pathlib import Path

from experiments.evaluate_c_reviews import load_and_validate
from src.evaluation.review_metrics import fingerprint, summarize
from src.utils.experiment_io import latest_records, read_records, sha256_file

ROOT = Path(__file__).resolve().parents[1]


def main():
    folder = ROOT / "docs/c_work"
    run = folder / "runs/policy_comparison_v1"
    manifest = json.loads((run / "manifest.json").read_text(encoding="utf-8"))
    contract = manifest["contract"]
    assert manifest["status"] == "completed" and not manifest["counts"]["errors"]
    for name in ("dataset", "controls", "corpus"):
        assert sha256_file(run / f"{name}.json") == contract[f"{name}_sha256"]
    for name, expected in contract["runtime_sha256"].items():
        assert sha256_file(run / "source_snapshot" / name) == expected
    rows = latest_records(read_records(run / "records.jsonl"))
    assert set(rows) == set(map(tuple, manifest["planned_records"]))
    assert len(rows) == 120
    program = [r for r in rows.values() if r["answer_origin"] == "policy_abstention"]
    assert len(program) == 5
    assert all(r["model_calls"] == 0 and r["output_tokens"] == 0 for r in program)
    old = {}
    for name in ("expanded_v3", "controls_v3"):
        old.update(latest_records(read_records(folder / "runs" / name / "records.jsonl")))
    legacy = [r for r in rows.values() if r["mode"] == "legacy"]
    assert len(legacy) == 40
    assert all((r["prompt"], r["answer"]) == (old[(str(r["id"]), "combined")]["prompt"], old[(str(r["id"]), "combined")]["answer"]) for r in legacy)
    reviews = load_and_validate([folder / "reviews/developer_reviews_v1.json"])
    human = summarize(reviews)
    assert len(reviews) == 84 and not human["tables"]
    mapping = json.loads((folder / "review_packet_v1_mapping.json").read_text(encoding="utf-8"))
    cache = {"policy_comparison_v1": rows}
    for name in ("expanded_v3", "controls_v3"):
        cache[name] = latest_records(read_records(folder / "runs" / name / "records.jsonl"))
    for item in mapping.values():
        assert fingerprint(cache[item["run"]][(str(item["id"]), item["mode"])]) == item["content_sha256"]
    for reviewer in ("C", "D"):
        with (folder / f"review_packet_v1/annotator_{reviewer}_blank.csv").open(encoding="utf-8-sig", newline="") as stream:
            blank = list(csv.DictReader(stream))
        assert {r["review_id"] for r in blank} == set(mapping)
        assert all(not value for r in blank for key, value in r.items() if key != "review_id")
    result = {"candidate_records": len(rows), "model_generated_answers": 115, "program_abstentions": len(program),
              "legacy_prompt_and_answer_replay": len(legacy), "ai_developer_review_records": len(reviews),
              "independent_human_reviews_completed": 0, "blank_records_per_annotator": len(mapping),
              "input_and_runtime_snapshots_verified": True, "packet_raw_hashes_verified": True,
              "original_dataset_sha256": sha256_file(ROOT / "datasets/hallucination/test_set.json")}
    assert result["original_dataset_sha256"] == "3477889ae807858e0763bce4c80534f7fc834e001a7136c7a47b0bd4f34892ed"
    (folder / "policy_verification.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
