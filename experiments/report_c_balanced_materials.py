"""Analyze balanced evidence judgments, source selection and material-position counterfactuals."""
import argparse
import copy
import csv
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from experiments.build_c_balanced_materials import LABELS, build_payload
from experiments.build_c_material_label_followup import TO_ZH, translate_payload
from experiments.check_c_source_bound import parse_object
from experiments.report_c_structured import analyze as analyze_structured
from experiments.report_c_suite import fenced
from src.utils.experiment_io import sha256_file

BASES = ("M1", "M2", "none")
SWAP = {"M1": "M2", "M2": "M1", "none": "none"}


def prediction(answer, label_map=None):
    parsed, encoding = None, "invalid"
    try:
        parsed, encoding = parse_object(answer.strip()), "bare_json"
    except (ValueError, TypeError):
        match = re.fullmatch(r"\s*```(?:json)?\s*\n?(.*?)\n?```\s*", answer, re.DOTALL | re.IGNORECASE)
        if match:
            try:
                parsed, encoding = parse_object(match.group(1).strip()), "fenced_json"
            except (ValueError, TypeError):
                pass
    verdict = parsed.get("verdict") if parsed is not None else None
    basis = parsed.get("basis") if parsed is not None else None
    mapping = label_map if label_map is not None else {label: label for label in LABELS}
    canonical = mapping.get(verdict) if type(verdict) is str else None
    return {"predicted_verdict": canonical if canonical in LABELS else "invalid",
            "predicted_label_raw": verdict if type(verdict) is str else None,
            "predicted_basis": basis if type(basis) is str and basis in BASES else "invalid", "parse_status": encoding}


def validate_design(payload):
    items = payload["items"]
    if len(items) != 48 or len({i["id"] for i in items}) != 48:
        raise ValueError("Expected 48 unique material-position variants")
    if Counter(i["expected_fields"]["verdict"] for i in items) != {label: 16 for label in LABELS}:
        raise ValueError("Three verdict classes must have sixteen variants each")
    if Counter(i["expected_fields"]["basis"] for i in items) != {label: 16 for label in BASES}:
        raise ValueError("Evidence positions and none must be balanced")
    pairs, topics = defaultdict(list), defaultdict(list)
    for item in items:
        pairs[item["case_pair_id"]].append(item)
        topics[item["contrast_group"]].append(item)
    if len(pairs) != 24 or len(topics) != 8 or any(len(v) != 6 for v in topics.values()):
        raise ValueError("Keep all related variants in their eight topic groups")
    for group in pairs.values():
        if len(group) != 2 or {i["position_variant"] for i in group} != {"base", "swapped"}:
            raise ValueError("Each statement needs exactly two position variants")
        a, b = sorted(group, key=lambda r: r["position_variant"])
        if a["claim"] != b["claim"] or [m["text"] for m in a["materials"]] != [m["text"] for m in reversed(b["materials"])]:
            raise ValueError("Position variants must not change the statement or material text")
        if a["expected_fields"]["verdict"] != b["expected_fields"]["verdict"] or SWAP[a["expected_fields"]["basis"]] != b["expected_fields"]["basis"]:
            raise ValueError("Evidence gold must track the material swap")


def aggregate(cases):
    groups = defaultdict(list)
    for case in cases:
        groups[case["mode"]].append(case)
    metrics, pairs, topics = [], [], []
    for mode, group in sorted(groups.items()):
        matrix = {label: {p: 0 for p in (*LABELS, "invalid")} for label in LABELS}
        for c in group:
            matrix[c["expected_verdict"]][c["predicted_verdict"]] += 1
        paired = defaultdict(list)
        topical = defaultdict(list)
        for c in group:
            paired[c["case_pair_id"]].append(c)
            topical[c["contrast_group"]].append(c)
        mode_pairs = []
        for pair_id, pair in sorted(paired.items()):
            if len(pair) != 2 or {p["position_variant"] for p in pair} != {"base", "swapped"}:
                raise ValueError("Do not compare unpaired or duplicate material positions")
            a, b = sorted(pair, key=lambda r: r["position_variant"])
            both_valid = a["predicted_verdict"] in LABELS and b["predicted_verdict"] in LABELS
            known = a["expected_verdict"] != "not_established"
            pair_result = {"mode": mode, "case_pair_id": pair_id, "contrast_group": a["contrast_group"],
                           "expected_verdict": a["expected_verdict"], "both_verdicts_valid": both_valid,
                           "verdict_unchanged": both_valid and a["predicted_verdict"] == b["predicted_verdict"],
                           "valid_verdict_changed": both_valid and a["predicted_verdict"] != b["predicted_verdict"],
                           "basis_tracks_swap": a["predicted_basis"] in BASES and b["predicted_basis"] == SWAP.get(a["predicted_basis"]),
                           "known_evidence_pair": known,
                           "known_basis_tracks_swap": known and a["predicted_basis"] in ("M1", "M2") and b["predicted_basis"] == SWAP.get(a["predicted_basis"]),
                           "both_joint_correct": a["joint_correct"] and b["joint_correct"],
                           "base_id": a["id"], "swapped_id": b["id"]}
            mode_pairs.append(pair_result)
            pairs.append(pair_result)
        for topic, topic_cases in sorted(topical.items()):
            topics.append({"mode": mode, "contrast_group": topic, "questions": len(topic_cases),
                           "verdict_correct": sum(c["verdict_correct"] for c in topic_cases),
                           "joint_correct": sum(c["joint_correct"] for c in topic_cases),
                           "all_verdicts_correct": all(c["verdict_correct"] for c in topic_cases),
                           "all_joint_correct": all(c["joint_correct"] for c in topic_cases)})
        metrics.append({"mode": mode, "policy": group[0]["policy"], "decoder": group[0]["decoder"], "questions": len(group),
                        "schema_conformant": sum(c["schema_conformant"] for c in group),
                        "valid_verdicts": sum(c["predicted_verdict"] in LABELS for c in group),
                        "invalid_verdicts": sum(c["predicted_verdict"] == "invalid" for c in group),
                        "verdict_correct": sum(c["verdict_correct"] for c in group),
                        "basis_correct": sum(c["basis_correct"] for c in group),
                        "joint_correct": sum(c["joint_correct"] for c in group),
                        "strict_task_passed": sum(c["strict_task_passed"] for c in group),
                        "unknown_as_supported": matrix["not_established"]["supported"],
                        "unknown_as_refuted": matrix["not_established"]["refuted"],
                        "supported_as_unknown": matrix["supported"]["not_established"],
                        "refuted_as_unknown": matrix["refuted"]["not_established"],
                        "unknown_questions": sum(c["expected_verdict"] == "not_established" for c in group),
                        "position_pairs": len(mode_pairs),
                        "both_verdicts_valid_pairs": sum(p["both_verdicts_valid"] for p in mode_pairs),
                        "verdict_unchanged_pairs": sum(p["verdict_unchanged"] for p in mode_pairs),
                        "valid_verdict_changed_pairs": sum(p["valid_verdict_changed"] for p in mode_pairs),
                        "basis_tracks_swap_pairs": sum(p["basis_tracks_swap"] for p in mode_pairs),
                        "known_evidence_pairs": sum(p["known_evidence_pair"] for p in mode_pairs),
                        "known_basis_tracks_swap_pairs": sum(p["known_basis_tracks_swap"] for p in mode_pairs),
                        "both_joint_correct_pairs": sum(p["both_joint_correct"] for p in mode_pairs),
                        "fully_joint_correct_topics": sum(t["all_joint_correct"] for t in topics if t["mode"] == mode),
                        "confusion_matrix": matrix})
    return metrics, pairs, topics


def analyze_balanced(run):
    base, rows = analyze_structured(run)
    manifest = json.loads((run / "manifest.json").read_text(encoding="utf-8"))
    if manifest["contract"]["config"].get("evidence_scope") != "question_only" or any(r["evidence"] for r in rows):
        raise ValueError("This comparison must exclude external retrieved evidence")
    payload = json.loads((run / "controls.json").read_text(encoding="utf-8"))
    label_map = payload.get("label_to_canonical", {label: label for label in LABELS})
    zh = payload.get("label_language") == "zh"
    if label_map != ({v: k for k, v in TO_ZH.items()} if zh else {label: label for label in LABELS}):
        raise ValueError("Label wording must use the declared complete semantic mapping")
    canonical_payload = copy.deepcopy(payload)
    for item in canonical_payload["items"]:
        item["expected_fields"]["verdict"] = label_map[item["expected_fields"]["verdict"]]
    validate_design(canonical_payload)
    protocol_path = ROOT / manifest["contract"]["config"].get("protocol", "docs/c_work/balanced_protocol_v1.json")
    protocol = json.loads(protocol_path.read_text(encoding="utf-8"))
    for name, expected in protocol["frozen_input_sha256"].items():
        if sha256_file(ROOT / name) != expected:
            raise ValueError("A predeclared material, schema or config file changed")
    specs_path = ROOT / "datasets/controls/c_balanced_material_specs.json"
    if payload["source_specs_sha256"] != sha256_file(specs_path):
        raise ValueError("Material source specification changed")
    rebuilt, schemas = build_payload(json.loads(specs_path.read_text(encoding="utf-8")))
    if zh:
        rebuilt, schemas = translate_payload(rebuilt, schemas)
    if payload["items"] != rebuilt["items"] or json.loads((run / "schemas.json").read_text(encoding="utf-8")) != schemas:
        raise ValueError("Frozen cases do not match the declared deterministic construction")
    by_id = {str(i["id"]): i for i in payload["items"]}
    checks = {(str(s["id"]), s["mode"]): s for s in base["checks"]}
    cases = []
    for row in rows:
        item = by_id[str(row["id"])]
        parsed = prediction(row["answer"], label_map)
        gold = item["expected_fields"]
        canonical_gold = label_map[gold["verdict"]]
        s = checks[(str(row["id"]), row["mode"])]
        v_correct, b_correct = parsed["predicted_verdict"] == canonical_gold, parsed["predicted_basis"] == gold["basis"]
        cases.append({"id": row["id"], "mode": row["mode"], "policy": row["policy"], "decoder": row["decoder"],
                      "contrast_group": item["contrast_group"], "topic_name": item["topic_name"],
                      "case_pair_id": item["case_pair_id"], "position_variant": item["position_variant"],
                      "expected_verdict": canonical_gold, "expected_label_raw": gold["verdict"], "expected_basis": gold["basis"], **parsed,
                      "verdict_correct": v_correct, "basis_correct": b_correct, "joint_correct": v_correct and b_correct,
                      "schema_conformant": s["schema_conformant"], "strict_task_passed": s["strict_task_passed"],
                      "truncated": row["truncated"], "content_sha256": s["content_sha256"]})
    metrics, pairs, topics = aggregate(cases)
    return {"stage": "balanced_supplied_material_development_diagnostic_not_independent_test",
            "design": payload["design"], "label_language": "zh" if zh else "en", "model_generated_answers": len(rows), "program_abstentions": 0,
            "independent_human_reviews": 0, "external_retrieved_passages": 0,
            "allowed_semantic_combinations": sorted(set(base["all_declared_combinations_per_task"].values())),
            "constant_class_verdict_baseline": {"correct": 16, "questions": 48},
            "formal_winner_selected": False, "metrics": metrics, "position_pairs": pairs, "topic_scores": topics,
            "costs": base["modes"], "cases": cases}, rows


def write_csv(path, rows, fields=None):
    if fields is None:
        fields = list(rows[0]) if rows else []
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def render_matrix(run, result):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    fig, axes = plt.subplots(2, 2, figsize=(11, 7.5), layout="constrained")
    wanted = ("legacy__free", "legacy__json", "compact__free", "compact__json")
    lookup = {m["mode"]: m for m in result["metrics"]}
    columns = (*LABELS, "invalid")
    for axis, mode in zip(axes.flat, wanted):
        m = lookup[mode]
        data = np.array([[m["confusion_matrix"][g][p] for p in columns] for g in LABELS])
        img = axis.imshow(data, cmap="Blues", vmin=0, vmax=16)
        axis.set_xticks(range(4), ["support", "refute", "not established", "invalid"], rotation=12)
        axis.set_yticks(range(3), ["support", "refute", "not established"])
        axis.set_title(f"{mode}: verdict {m['verdict_correct']}/48; joint {m['joint_correct']}/48", fontsize=11)
        axis.set_xlabel("Parsed output label")
        axis.set_ylabel("Provided-material expectation")
        for i in range(3):
            for j in range(4):
                axis.text(j, i, str(data[i, j]), ha="center", va="center", color="white" if data[i, j] > 8 else "black")
    fig.colorbar(img, ax=axes, shrink=.8, label="Count (16 per expected class)")
    fig.suptitle(f"Developer diagnostics ({result['label_language']} labels): 24 claims x 2 positions; 8 related topics", fontsize=12)
    output = run / "figures/confusion_matrix.png"
    output.parent.mkdir(exist_ok=True)
    fig.savefig(output, dpi=180)
    plt.close(fig)
    return {"path": "figures/confusion_matrix.png", "sha256": sha256_file(output), "matplotlib": matplotlib.__version__}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run", nargs="?", type=Path, default=ROOT / "docs/c_work/runs/balanced_materials_v1")
    args = parser.parse_args()
    result, rows = analyze_balanced(args.run)
    result["figure"] = render_matrix(args.run, result)
    result["evaluation_sources"] = {}
    for name in ("experiments/report_c_balanced_materials.py", "experiments/report_c_structured.py", "experiments/build_c_material_label_followup.py",
                 "experiments/check_c_source_bound.py", "experiments/build_c_balanced_materials.py"):
        digest = sha256_file(ROOT / name)
        relative = f"evaluation_snapshot/{Path(name).stem}-{digest[:12]}.py"
        path = args.run / relative
        path.parent.mkdir(exist_ok=True)
        path.write_bytes((ROOT / name).read_bytes())
        result["evaluation_sources"][relative] = digest
    (args.run / "balanced_checks.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    write_csv(args.run / "metrics.csv", result["metrics"], [k for k in result["metrics"][0] if k != "confusion_matrix"])
    write_csv(args.run / "case_checks.csv", result["cases"])
    write_csv(args.run / "position_pairs.csv", result["position_pairs"])
    write_csv(args.run / "topic_scores.csv", result["topic_scores"])
    by_id = {str(i["id"]): i for i in json.loads((args.run / "controls.json").read_text(encoding="utf-8"))["items"]}
    case_lookup = {(str(c["id"]), c["mode"]): c for c in result["cases"]}
    label_scope = "中文标签；这是观察到英文结果后追加、在中文生成前冻结的探索性对照。" if result["label_language"] == "zh" else "英文标签；评分计划在该轮生成前冻结。"
    lines = ["# 均衡材料判断与位置交换诊断", "", label_scope, "", "本轮先冻结8个主题、24条陈述，每条陈述做两个材料位置变体，共48题；支持、反驳、证据不足各16题，依据M1、M2、none也各16题。两种提示乘两种解码生成192条模型回答，未调用外部检索。", "",
             "这些是开发者按已有来源整理的材料任务。48个变体并非48个独立事实题，相关单位为8个主题；不作为原不确定性探针真值、独立测试或最终验收成绩。三类均衡时，总选同一类只能得到16/48的结论符合。", "",
             "## 格式、结论与依据", "", "| 条件 | 结构符合 | 结论符合 | 依据符合 | 两者同时符合 | 严格任务符合 | 无效结论 |", "| --- | ---: | ---: | ---: | ---: | ---: | ---: |"]
    for m in result["metrics"]:
        lines.append(f"| {m['mode']} | {m['schema_conformant']}/48 | {m['verdict_correct']}/48 | {m['basis_correct']}/48 | {m['joint_correct']}/48 | {m['strict_task_passed']}/48 | {m['invalid_verdicts']}/48 |")
    lines.extend(["", "结论和依据可从完整JSON或完整代码围栏内对象读取，额外键只影响结构与严格任务；零散JSON或无效语法不猜测恢复。无效结论单列，未通过检查不表示整段事实全部错误。JSON约束固定格式、保留全部9种值组合，不能把结构保证当作事实判断可靠。", "",
                  "![三类混淆矩阵](figures/confusion_matrix.png)", "", "## 证据不足与错误判断", "",
                  "| 条件 | 不足误判支持/16 | 不足误判反驳/16 | 有支持漏判不足/16 | 有反驳漏判不足/16 |", "| --- | ---: | ---: | ---: | ---: |"])
    for m in result["metrics"]:
        lines.append(f"| {m['mode']} | {m['unknown_as_supported']} | {m['unknown_as_refuted']} | {m['supported_as_unknown']} | {m['refuted_as_unknown']} |")
    lines.extend(["", "## 交换材料位置", "", "| 条件 | 两位置均有有效结论/24 | 结论不变/24 | 有依据时编号跟随/16 | 两位置都同时判对结论和依据/24 | 全主题同时符合/8 |", "| --- | ---: | ---: | ---: | ---: | ---: |"])
    for m in result["metrics"]:
        lines.append(f"| {m['mode']} | {m['both_verdicts_valid_pairs']} | {m['verdict_unchanged_pairs']} | {m['known_basis_tracks_swap_pairs']} | {m['both_joint_correct_pairs']} | {m['fully_joint_correct_topics']} |")
    lines.extend(["", "结论稳定不等于结论正确；一直选不足可能稳定却遗漏全部可回答项。依据编号按实际位置交换核对，不能要求M1/M2字符串不变。有效结论的配对覆盖率、两位置都正确和主题级结果分别保留，不计算假定48题相互独立的显著性。", "",
                  "## 原始回答与检查", "", "[逐条检查](case_checks.csv)、[位置配对](position_pairs.csv)、[主题结果](topic_scores.csv)、[原始日志](records.jsonl)。所有192条保留，四个条件的完整材料与回答分别列出：", ""])
    (args.run / "cases").mkdir(exist_ok=True)
    for mode in sorted({r["mode"] for r in rows}):
        path = args.run / "cases" / (mode + ".md")
        case_lines = ["# " + mode, "", "自动规则检查，未完成人工复核。", ""]
        for row in rows:
            if row["mode"] != mode:
                continue
            item = by_id[str(row["id"])]
            c = case_lookup[(str(row["id"]), mode)]
            case_lines.extend([f"## {row['id']} / {item['topic_name']} / {item['position_variant']}", "", row["question"], "", fenced(row["answer"]), "",
                               "冻结预期：" + json.dumps(item["expected_fields"], ensure_ascii=False), "自动检查：" + json.dumps(c, ensure_ascii=False), ""])
        path.write_text("\n".join(case_lines), encoding="utf-8")
        lines.append(f"- [{mode}](cases/{mode}.md)")
    lines.extend(["", "## 使用边界", "", "此轮补清了字段指代并平衡三类样本，来源选择和材料顺序另作检查。仍由同一开发流程构造，缺少独立人工评分和独立材料集；不得依据局部数值替换默认治理或宣称总体幻觉降低。运行配置和评分计划在生成前保存，失败回答和截断均保留。", ""])
    (args.run / "report.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"design": result["design"], "records": len(rows), "metrics": result["metrics"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
