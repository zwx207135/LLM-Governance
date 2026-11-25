"""Import completed annotations with explicit reviewer identity; reject empty templates."""
import argparse
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from experiments.evaluate_c_reviews import sources
from src.evaluation.review_metrics import LABELS, validate_review
from src.utils.experiment_io import latest_records, read_records


def import_rows(rows, mapping, reviewer_id, reviewer_type, records, valid_sources):
    if not reviewer_id.strip() or reviewer_type not in ("human", "ai_developer"):
        raise ValueError("Explicit reviewer identity and type required")
    result, seen = [], set()
    for row in rows:
        if not any(row.get(k, "").strip() for k in list(LABELS) + ["source_ids", "rationale"]):
            continue
        ident = row["review_id"]
        if ident in seen:
            raise ValueError("Duplicate review_id")
        seen.add(ident)
        entry = mapping[ident]
        review = {**entry, "reviewer_id": reviewer_id, "reviewer_type": reviewer_type,
                  **{k: row.get(k, "").strip() for k in LABELS},
                  "source_ids": [s.strip() for s in row.get("source_ids", "").split(";") if s.strip()],
                  "rationale": row.get("rationale", "").strip(), "review_origin": "explicit_annotation_import"}
        record = records[(entry["run"], str(entry["id"]), entry["mode"])]
        validate_review(review, record, valid_sources)
        result.append(review)
    if not result:
        raise ValueError("No completed annotations; empty forms are not reviews")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", type=Path)
    parser.add_argument("--mapping", type=Path, default=ROOT / "docs/c_work/review_packet_v1_mapping.json")
    parser.add_argument("--reviewer-id", required=True)
    parser.add_argument("--reviewer-type", choices=("human", "ai_developer"), required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError("Use a new annotation filename; original judgments are retained")
    mapping = json.loads(args.mapping.read_text(encoding="utf-8"))
    records = {}
    for run in {v["run"] for v in mapping.values()}:
        for key, value in latest_records(read_records(ROOT / "docs/c_work/runs" / run / "records.jsonl")).items():
            records[(run, *key)] = value
    with args.csv.open(encoding="utf-8-sig", newline="") as stream:
        reviews = import_rows(list(csv.DictReader(stream)), mapping, args.reviewer_id, args.reviewer_type, records, sources())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps({"protocol_version": "c-review-v1", "reviews": reviews}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Imported {len(reviews)} attributed reviews")


if __name__ == "__main__":
    main()
