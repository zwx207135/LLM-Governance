"""Compare exploratory label translations with paired materials, claims and model conditions."""
import json
from pathlib import Path

from experiments.build_c_material_label_followup import translate_payload
from experiments.report_c_balanced_materials import analyze_balanced
from src.utils.experiment_io import sha256_file

ROOT = Path(__file__).resolve().parents[1]


def compare_runs(english_run, chinese_run):
    en, _ = analyze_balanced(english_run)
    zh, _ = analyze_balanced(chinese_run)
    en_data = json.loads((english_run / "controls.json").read_text(encoding="utf-8"))
    en_schemas = json.loads((english_run / "schemas.json").read_text(encoding="utf-8"))
    translated, translated_schemas = translate_payload(en_data, en_schemas)
    if translated != json.loads((chinese_run / "controls.json").read_text(encoding="utf-8")) or translated_schemas != json.loads((chinese_run / "schemas.json").read_text(encoding="utf-8")):
        raise ValueError("Label follow-up must preserve evidence, statements and position variants")
    a = json.loads((english_run / "manifest.json").read_text(encoding="utf-8"))["contract"]
    b = json.loads((chinese_run / "manifest.json").read_text(encoding="utf-8"))["contract"]
    for field in ("model_sha256", "runtime_sha256", "python"):
        if a[field] != b[field]:
            raise ValueError("Model/runtime changed between label conditions")
    for field in ("policies", "decoders", "generation", "seed", "evidence_scope", "retrieval"):
        if a["config"][field] != b["config"][field]:
            raise ValueError("Generation settings changed beyond label wording")
    e_cases = {(c["id"], c["mode"]): c for c in en["cases"]}
    z_cases = {(c["id"], c["mode"]): c for c in zh["cases"]}
    if set(e_cases) != set(z_cases):
        raise ValueError("Different case/condition coverage")
    z_metrics = {m["mode"]: m for m in zh["metrics"]}
    table = []
    for e in en["metrics"]:
        z = z_metrics[e["mode"]]
        pairs = [(c, z_cases[key]) for key, c in e_cases.items() if c["mode"] == e["mode"]]
        table.append({"mode": e["mode"], "paired_questions": len(pairs),
                      "en_verdict_correct": e["verdict_correct"], "zh_verdict_correct": z["verdict_correct"],
                      "en_joint_correct": e["joint_correct"], "zh_joint_correct": z["joint_correct"],
                      "en_unknown_as_supported": e["unknown_as_supported"], "zh_unknown_as_supported": z["unknown_as_supported"],
                      "en_only_verdict_correct": sum(x["verdict_correct"] and not y["verdict_correct"] for x, y in pairs),
                      "zh_only_verdict_correct": sum(y["verdict_correct"] and not x["verdict_correct"] for x, y in pairs),
                      "both_verdict_correct": sum(x["verdict_correct"] and y["verdict_correct"] for x, y in pairs),
                      "neither_verdict_correct": sum(not x["verdict_correct"] and not y["verdict_correct"] for x, y in pairs),
                      "en_schema_conformant": e["schema_conformant"], "zh_schema_conformant": z["schema_conformant"]})
    return {"stage": "exploratory_label_wording_followup_not_independent_evaluation", "model_generated_answers": 384,
            "unique_claims": 24, "topic_groups": 8, "same_materials_claims_and_positions": True,
            "same_model_runtime_and_generation_settings": True, "independent_human_reviews": 0,
            "formal_winner_selected": False, "comparison": table,
            "limits": "Follow-up added after observing English-label bias; label translation changes tokenization and language priors. Eight related topics, not 384 independent facts."}


def main():
    folder = ROOT / "docs/c_work"
    en = folder / "runs/balanced_materials_v1"
    zh = folder / "runs/balanced_labels_cn_v1"
    result = compare_runs(en, zh)
    result["input_record_sha256"] = {run.name: sha256_file(run / "records.jsonl") for run in (en, zh)}
    (folder / "material_label_comparison.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = ["# 材料判断：英文与中文标签探索性对照", "", "先完成英文192条，观察到明显supported偏向后，追加中文标签192条。中文生成前冻结了追加计划；不是原计划中的预注册结果。两轮材料、陈述、位置、模型、运行源码、生成设置全部相同，只翻译指令中的结论标签和schema枚举。", "",
             "48个材料位置变体来自24条陈述、8个相关主题，不能按384个独立事实样本解释。两轮均关闭外部检索，正确答案不进入生成；schema保留全部9种结论与依据组合。", "",
             "| 条件 | 英文结论符合/48 | 中文结论符合/48 | 英文结论及依据均符合/48 | 中文结论及依据均符合/48 |", "| --- | ---: | ---: | ---: | ---: |"]
    for row in result["comparison"]:
        lines.append(f"| {row['mode']} | {row['en_verdict_correct']} | {row['zh_verdict_correct']} | {row['en_joint_correct']} | {row['zh_joint_correct']} |")
    lines.extend(["", "结论符合和依据符合分别计算，完整JSON或完整围栏内对象的合法字段可进入内容检查；无效输出另列。结构符合仍是不同维度，不能由它推出内容正确。总选同一结论的基线为16/48。", "",
                  "## 同一题成对变化", "", "| 条件 | 仅英文结论符合 | 仅中文结论符合 | 两者符合 | 两者均不符合 | 英文不足误判支持/16 | 中文不足误判支持/16 |", "| --- | ---: | ---: | ---: | ---: | ---: | ---: |"])
    for row in result["comparison"]:
        lines.append(f"| {row['mode']} | {row['en_only_verdict_correct']} | {row['zh_only_verdict_correct']} | {row['both_verdict_correct']} | {row['neither_verdict_correct']} | {row['en_unknown_as_supported']} | {row['zh_unknown_as_supported']} |")
    lines.extend(["", "## 混淆矩阵及逐条记录", "", "[英文报告](runs/balanced_materials_v1/report.md) · [中文报告](runs/balanced_labels_cn_v1/report.md)", "",
                  "![英文标签](runs/balanced_materials_v1/figures/confusion_matrix.png)", "",
                  "![中文标签](runs/balanced_labels_cn_v1/figures/confusion_matrix.png)", "",
                  "标签语言可能改变模型的输出偏好、token路径与任务理解；本轮不能据此确认内部机制。保留全部成功、失败和位置变体，不据探索性结果替换默认治理。真实人工评分仍为0。", ""])
    (folder / "material_label_comparison.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
