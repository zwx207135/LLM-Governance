"""Check review provenance against immutable raw answers and compile scoped metrics."""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.evaluation.review_metrics import summarize, validate_review
from src.utils.experiment_io import latest_records, read_records


def sources():
    corpus = json.loads((ROOT / "knowledge/corpus_v3.json").read_text(encoding="utf-8"))
    registry = json.loads((ROOT / "docs/c_work/source_registry.json").read_text(encoding="utf-8-sig"))
    extra = json.loads((ROOT / "docs/c_work/review_sources.json").read_text(encoding="utf-8"))
    followup = json.loads((ROOT / "docs/c_work/source_followup_v1.json").read_text(encoding="utf-8"))
    material_mapping = ROOT / "docs/c_work/review_packet_materials_v1_mapping.json"
    material_ids = json.loads(material_mapping.read_text(encoding="utf-8")) if material_mapping.exists() else {}
    return {s["id"] for s in corpus["sources"] + registry["sources"] + extra["sources"] + followup["sources"]} | {f"math:{i}" for i in range(101, 126)} | {f"task:N{i:02d}" for i in range(1, 21)} | {f"task:materials_v1:{ident}" for ident in material_ids} | {"internal:answer"}


def load_and_validate(paths):
    reviews, cache = [], {}
    valid = sources()
    for path in paths:
        payload = json.loads(path.read_text(encoding="utf-8"))
        for review in payload["reviews"]:
            run = review["run"]
            if Path(run).name != run:
                raise ValueError("Run must be a registered directory name")
            if run not in cache:
                cache[run] = latest_records(read_records(ROOT / "docs/c_work/runs" / run / "records.jsonl"))
            record = cache[run][(str(review["id"]), review["mode"])]
            validate_review(review, record, valid)
            reviews.append(review)
    return reviews


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("annotations", nargs="+", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--include-ai", action="store_true", help="Explicitly produce a developer-only preliminary analysis")
    args = parser.parse_args()
    reviews = load_and_validate(args.annotations)
    result = summarize(reviews, args.include_ai)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
