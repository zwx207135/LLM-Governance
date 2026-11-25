"""Create empty reviewer forms for two complete topic groups across both label languages."""
import csv
import json
import random
from pathlib import Path

from experiments.report_c_suite import fenced
from src.evaluation.review_metrics import LABELS, fingerprint
from src.utils.experiment_io import latest_records, read_records

ROOT = Path(__file__).resolve().parents[1]


def main():
    folder = ROOT / "docs/c_work"
    output = folder / "review_packet_materials_v1"
    mapping_path = folder / "review_packet_materials_v1_mapping.json"
    if output.exists() or mapping_path.exists():
        raise FileExistsError("Use new packet names; reviewer forms are never overwritten")
    payload = json.loads((folder / "runs/balanced_materials_v1/controls.json").read_text(encoding="utf-8"))
    rng = random.Random(20261122)
    topics = rng.sample(sorted({i["contrast_group"] for i in payload["items"]}), 2)
    selected = []
    for name in ("balanced_materials_v1", "balanced_labels_cn_v1"):
        run = folder / "runs" / name
        controls = json.loads((run / "controls.json").read_text(encoding="utf-8"))
        items = {str(i["id"]): i for i in controls["items"]}
        for row in latest_records(read_records(run / "records.jsonl")).values():
            if items[str(row["id"])]["contrast_group"] in topics:
                selected.append((name, row))
    rng.shuffle(selected)
    if len(selected) != 96:
        raise ValueError("Expected 96 outputs preserving complete topic/label/position/decoder groups")
    mapping, lines = {}, ["# 材料任务独立复核", "", "隐藏显式策略与解码条件名，保留完整问题及回答。语言、措辞和格式可能暴露条件，并非完全盲化。不附自动评分标签，先各自判断。", ""]
    for number, (name, row) in enumerate(selected, 1):
        ident = f"RB{number:04d}"
        mapping[ident] = {"run": name, "id": row["id"], "mode": row["mode"], "content_sha256": fingerprint(row),
                          "data_role": row["data_role"], "answer_origin": row["answer_origin"]}
        lines.extend([f"## {ident}", "", row["question"], "", "输出来源：model。", "", fenced(row["answer"]), ""])
    output.mkdir()
    (output / "items.md").write_text("\n".join(lines), encoding="utf-8")
    mapping_path.write_text(json.dumps(mapping, ensure_ascii=False, indent=2), encoding="utf-8")
    fields = ["review_id", *LABELS, "source_ids", "rationale"]
    for reviewer in ("C", "D"):
        with (output / f"annotator_{reviewer}_blank.csv").open("w", encoding="utf-8-sig", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=fields)
            writer.writeheader()
            writer.writerows({"review_id": key} for key in mapping)
    manifest = {"stage": "empty_independent_review_materials", "topic_groups": sorted(topics),
                "topic_coverage": "2/8 groups (25%); all three classes, both positions, four conditions and two label languages retained",
                "template_records_per_annotator": len(mapping), "independent_human_reviews_completed": 0,
                "selection": "Deterministic development quality review; not an independent population-effect estimate"}
    (output / "packet_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    (output / "README.md").write_text("""# 本轮材料复核填写说明

本包为C、D各96项空白表，抽取完整2/8主题组，保留三种结论、两种材料位置、四种生成条件及中英文标签。当前人工复核完成数为0；模板不是评分成果。

先阅读上级REVIEW_PROTOCOL.md及C_REVIEW_WORKFLOW.md，再各自阅读items.md、填写CSV。不要先看balanced_checks或对比报告中的自动标签。对任务完成度、格式、实际证据支持和附加解释分开判断；没有填对字段不代表所有事实错误，填对结论也不代表依据正确。source_ids可使用题目材料对应的已登记来源ID；原始来源汇总在datasets/controls/c_balanced_material_specs.json及source_followup_v1/report.md。

另存completed_materials_C.csv、completed_materials_D.csv后，在仓库根目录执行：

```powershell
python -m experiments.import_c_annotations completed_materials_C.csv --mapping docs/c_work/review_packet_materials_v1_mapping.json --reviewer-id actual_C --reviewer-type human --output docs/c_work/reviews/materials_C_v1.json
python -m experiments.import_c_annotations completed_materials_D.csv --mapping docs/c_work/review_packet_materials_v1_mapping.json --reviewer-id actual_D --reviewer-type human --output docs/c_work/reviews/materials_D_v1.json
python -m experiments.reconcile_c_reviews docs/c_work/reviews/materials_C_v1.json docs/c_work/reviews/materials_D_v1.json --output docs/c_work/reconciliation_materials_round1
```

身份使用真实负责者的稳定ID，不用同一人充当两人。不把裁决后意见算作第三份独立意见。措辞与输出语言可能暴露条件，不能宣称完全盲化；分组抽样仅供开发质量复核。
""", encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
