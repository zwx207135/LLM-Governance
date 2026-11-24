"""Bind explicitly authored AI developer judgments to exact immutable answer hashes."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from experiments.evaluate_c_reviews import sources
from src.evaluation.review_metrics import fingerprint, validate_review
from src.utils.experiment_io import latest_records, read_records


def main():
    folder = ROOT / "docs/c_work/reviews"
    notes = json.loads((folder / "developer_notes_v1.json").read_text(encoding="utf-8"))
    old = latest_records(read_records(ROOT / "docs/c_work/runs/expanded_v3/records.jsonl"))
    new = latest_records(read_records(ROOT / "docs/c_work/runs/policy_comparison_v1/records.jsonl"))
    valid_sources = sources()
    reviews = []
    def make(run, record, values, source_ids, origin="direct_AI_developer_review"):
        review = {"run": run, "id": record["id"], "mode": record["mode"], "content_sha256": fingerprint(record),
                  "reviewer_id": notes["reviewer_id"], "reviewer_type": notes["reviewer_type"],
                  "review_origin": origin, "protocol_version": "c-review-v1", "source_ids": source_ids,
                  "data_role": record["data_role"], **dict(zip(notes["columns"], values))}
        validate_review(review, record, valid_sources)
        reviews.append(review)
        return review
    for ident, detail in notes["old_run"].items():
        for mode, values in detail["modes"].items():
            make("expanded_v3", old[(ident, mode)], values, detail["sources"])
    for ident, values in notes["compact"].items():
        detail = notes["old_run"][ident]
        legacy = new[(ident, "legacy")]
        previous = old[(ident, "combined")]
        if legacy["answer"] != previous["answer"] or legacy["question"] != previous["question"]:
            raise ValueError("Legacy output changed; requires a fresh explicit judgment")
        make("policy_comparison_v1", legacy, detail["modes"]["combined"], detail["sources"], "reused_identical_legacy_answer_AI_developer")
        compact = new[(ident, "compact")]
        make("policy_comparison_v1", compact, values, detail["sources"])
        guarded = new[(ident, "guarded")]
        if ident in notes["guarded_overrides"]:
            guard_values = notes["guarded_overrides"][ident]
            origin = "direct_AI_developer_review"
        else:
            if guarded["answer"] != compact["answer"] or guarded["question"] != compact["question"]:
                raise ValueError("Guarded output differs; needs a fresh explicit judgment")
            guard_values, origin = values, "reused_identical_compact_answer_AI_developer"
        make("policy_comparison_v1", guarded, guard_values, detail["sources"], origin)
    target = folder / "developer_reviews_v1.json"
    target.write_text(json.dumps({"protocol_version": "c-review-v1", "selection": notes["selection"],
                                 "independent_human_reviews": 0, "reviews": reviews}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(reviews)} AI developer review records; independent human reviews: 0")


if __name__ == "__main__":
    main()
