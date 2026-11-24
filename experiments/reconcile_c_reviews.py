"""Prepare or apply explicit human adjudication while retaining every original judgment."""
import argparse
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from experiments.evaluate_c_reviews import load_and_validate, sources
from experiments.report_c_suite import fenced
from src.evaluation.reconciliation import identity, reconcile
from src.evaluation.review_metrics import LABELS
from src.utils.experiment_io import latest_records, read_records, sha256_file

RUNTIME = ("experiments/reconcile_c_reviews.py", "experiments/evaluate_c_reviews.py",
           "experiments/report_c_suite.py", "src/evaluation/reconciliation.py",
           "src/evaluation/review_metrics.py", "src/utils/experiment_io.py")


def load_raw_records(reviews):
    records = {}
    for run in {r["run"] for r in reviews}:
        for (ident, mode), row in latest_records(read_records(ROOT / "docs/c_work/runs" / run / "records.jsonl")).items():
            records[(run, ident, mode)] = row
    return records


def write_materials(output, result, records):
    with (output / "adjudication_blank.csv").open("w", encoding="utf-8-sig", newline="") as stream:
        fields = ["resolution_id", "review_group_sha256", *LABELS, "source_ids", "rationale"]
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        completed = {r["resolution_id"] for r in result["resolved_records"]}
        writer.writerows({k: group[k] for k in ("resolution_id", "review_group_sha256")}
                         for group in result["review_groups"] if group["state"] == "conflict" and group["resolution_id"] not in completed)
    lines = ["# 双人复核与裁决记录", "", "先由两位标注者独立提交，再处理分歧。本材料保留原意见；裁决后的意见不用于重算原始一致性。", "",
             "当前状态：" + result["report"]["status"], "",
             f"独立人工意见{result['report']['human_judgment_records']}条，排除AI意见{result['report']['ai_judgments_excluded']}条；已形成最终标签的回答{result['report']['resolved_answers']}条。", ""]
    for group in result["review_groups"]:
        row = records[identity(group)]
        differences = ", ".join(group["disagreement_dimensions"]) or ("尚需第二人" if group["state"] == "single_review" else "无")
        lines.extend([f"## {group['resolution_id']}", "", f"{group['run']} / {group['id']} / {group['mode']}；状态{group['state']}。", "",
                      row["question"], "", fenced(row["answer"]), "",
                      "分歧维度：" + differences, ""])
        for review in group["original_reviews"]:
            lines.extend(["原始标注者：" + review["reviewer_id"], "",
                          json.dumps({k: review[k] for k in LABELS}, ensure_ascii=False), "",
                          "依据：" + "; ".join(review["source_ids"]), review["rationale"], ""])
        for evidence in row.get("evidence", []):
            lines.extend([f"模型所见资料 {evidence['id']}：{evidence['text']}", evidence["source"]["url"], ""])
    (output / "report.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("annotations", nargs="+", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--decisions", type=Path)
    parser.add_argument("--adjudicator-id")
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError("Use a new resolution directory; original reviews and adjudication outputs are retained")
    if args.decisions and not args.adjudicator_id:
        parser.error("--decisions requires --adjudicator-id declaring the human adjudicator")
    reviews = load_and_validate(args.annotations)
    records = load_raw_records(reviews)
    decisions = None
    if args.decisions:
        with args.decisions.open(encoding="utf-8-sig", newline="") as stream:
            decisions = list(csv.DictReader(stream))
    result = reconcile(reviews, decisions, args.adjudicator_id, records, sources())
    args.output.mkdir(parents=True)
    inputs = []
    for index, path in enumerate(args.annotations):
        name = f"original_annotations_{index:02d}.json"
        (args.output / name).write_bytes(path.read_bytes())
        inputs.append({"snapshot": name, "original_path": str(path), "sha256": sha256_file(path)})
    if args.decisions:
        (args.output / "submitted_decisions.csv").write_bytes(args.decisions.read_bytes())
    for relative in RUNTIME:
        snapshot = args.output / "source_snapshot" / relative
        snapshot.parent.mkdir(parents=True, exist_ok=True)
        snapshot.write_bytes((ROOT / relative).read_bytes())
    manifest = {"protocol": "c-two-human-resolution-v1", "annotation_inputs": inputs,
                "decisions_sha256": sha256_file(args.decisions) if args.decisions else None,
                "adjudicator_id": args.adjudicator_id,
                "runtime_sha256": {p: sha256_file(ROOT / p) for p in RUNTIME}}
    (args.output / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    (args.output / "review_state.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    write_materials(args.output, result, records)
    print(json.dumps(result["report"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
