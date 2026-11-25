"""Create two EMPTY blinded review forms; do not manufacture independent annotations."""
import csv
import argparse
import json
import math
import random
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from experiments.report_c_suite import fenced
from src.evaluation.review_metrics import LABELS, fingerprint
from src.utils.experiment_io import latest_records, read_records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--refresh-documents", action="store_true", help="Rebuild readable materials without touching either annotation CSV")
    args = parser.parse_args()
    output = ROOT / "docs/c_work/review_packet_v1"
    if args.refresh_documents:
        if not output.is_dir():
            raise FileNotFoundError("Create the packet before refreshing")
    else:
        output.mkdir(exist_ok=False)
    rng = random.Random(20261122)
    config = json.loads((ROOT / "configs/c_policy_comparison.json").read_text(encoding="utf-8"))
    selected, coverage = [], []
    for run_name in ("expanded_v3", "controls_v3", "policy_comparison_v1"):
        run = ROOT / "docs/c_work/runs" / run_name
        rows = list(latest_records(read_records(run / "records.jsonl")).values())
        dataset = json.loads((run / "dataset.json").read_text(encoding="utf-8"))["items"]
        if (run / "controls.json").exists():
            dataset += json.loads((run / "controls.json").read_text(encoding="utf-8"))["items"]
        samples = {str(i["id"]): i for i in dataset}
        strata = defaultdict(set)
        for row in rows:
            strata[row["category"]].add(str(row["id"]))
        chosen = set()
        for category, ids in sorted(strata.items()):
            ids = sorted(ids)
            chosen.update(rng.sample(ids, math.ceil(len(ids) * .2)))
        if run_name in ("expanded_v3", "policy_comparison_v1"):
            chosen.update(str(i) for i in config["review_ids"])
        part = [r for r in rows if str(r["id"]) in chosen]
        coverage.append({"run": run_name, "available_records": len(rows), "selected_records": len(part),
                         "selected_question_groups": len(chosen), "coverage": len(part) / len(rows)})
        for row in part:
            selected.append((run_name, row, samples[str(row["id"])]))
    rng.shuffle(selected)
    mapping, lines = {}, ["# 独立复核材料", "", "本材料隐藏显式策略名，评分表为空。不要先看相邻目录中的AI开发复核标签。措辞仍可能暴露策略，因此不是完全盲化。", ""]
    for number, (run_name, row, item) in enumerate(selected, 1):
        ident = f"R{number:04d}"
        mapping[ident] = {"run": run_name, "id": row["id"], "mode": row["mode"],
                          "content_sha256": fingerprint(row), "data_role": row["data_role"],
                          "answer_origin": row.get("answer_origin", "model")}
        reference = ("任务复核要点：" + item["review_checklist"] + f"；材料证据ID：task:{row['id']}。") if row["category"] == "normal_control" else (
            "候选参考：" + (item.get("reference") or "本题未建立事实真值，不按不存在断言评分。"))
        lines.extend([f"## {ident}", "", row["question"], "", f"输出来源：{row.get('answer_origin', 'model')}。", "",
                      "回答：", "", fenced(row["answer"]), "",
                      reference, ""])
        for h in row.get("evidence", []):
            lines.extend([f"提供给回答方的资料：{h['text']}", f"来源ID {h['source_id']}：{h['source']['url']}", ""])
        if row["category"] == "math_logic":
            lines.extend([f"推导证据ID：math:{row['id']}；详见data_audit.json。", ""])
        if item.get("evidence_urls"):
            lines.extend(["候选参考来源：" + "; ".join(item["evidence_urls"]), ""])
    if args.refresh_documents:
        old_mapping = json.loads((output.parent / "review_packet_v1_mapping.json").read_text(encoding="utf-8"))
        if old_mapping != mapping:
            raise ValueError("Packet identity/order changed; create a new packet version instead")
        (output / "items.md").write_text("\n".join(lines), encoding="utf-8")
        print("Readable materials refreshed; annotation CSVs and mapping unchanged")
        return
    (output / "items.md").write_text("\n".join(lines), encoding="utf-8")
    # The mapping is outside the blinded folder.
    (output.parent / "review_packet_v1_mapping.json").write_text(json.dumps(mapping, ensure_ascii=False, indent=2), encoding="utf-8")
    fields = ["review_id"] + list(LABELS) + ["source_ids", "rationale"]
    for annotator in ("C", "D"):
        with (output / f"annotator_{annotator}_blank.csv").open("w", encoding="utf-8-sig", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=fields)
            writer.writeheader()
            writer.writerows({"review_id": ident} for ident in mapping)
    summary = {"template_records_per_annotator": len(mapping), "independent_human_reviews_completed": 0,
               "sampling": "20% question groups per category plus predeclared disputed cases; keep all modes in a group",
               "coverage": coverage, "labels": {k: sorted(v) for k, v in LABELS.items()}}
    (output / "packet_manifest.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    (output / "README.md").write_text("# 独立复核填写说明\n\n先阅读相邻的REVIEW_PROTOCOL.md，再分别打开items.md和自己的空白CSV。source_ids使用来源登记ID或math:样本ID，多个ID用分号隔开；每条填写理由。\n\n不要复制另一人的标签或AI开发者判断。填完后用import_c_annotations导入，再用evaluate_c_reviews比较；分歧在裁决前保留。映射文件在本目录之外，不需要提前打开。模板数量不表示已完成标注。\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in summary.items() if k != "labels"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
