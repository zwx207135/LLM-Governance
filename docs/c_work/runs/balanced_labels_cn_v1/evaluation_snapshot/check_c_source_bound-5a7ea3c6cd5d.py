"""Grade five frozen, supplied-material diagnostics; do not infer truth of original entity probes."""
import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from experiments.report_c_policy_comparison import load_comparison
from experiments.report_c_suite import fenced
from src.utils.experiment_io import sha256_file, stable_hash


def parse_object(text):
    def object_pairs(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("Duplicate JSON key")
            result[key] = value
        return result

    def reject_constant(value):
        raise ValueError("Nonfinite values are not JSON")

    value = json.loads(text, object_pairs_hook=object_pairs, parse_constant=reject_constant)
    if not isinstance(value, dict):
        raise ValueError("A JSON object is required")
    return value


def check_answer(answer, expected):
    if not isinstance(answer, str):
        raise ValueError("Only actual answer text can be checked")
    strict, parsed, wrapped = False, None, False
    try:
        parsed = parse_object(answer.strip())
        strict = True
    except (ValueError, TypeError):
        match = re.fullmatch(r"\s*```(?:json)?\s*\n?(.*?)\n?```\s*", answer, re.DOTALL | re.IGNORECASE)
        if match:
            try:
                parsed = parse_object(match.group(1).strip())
                wrapped = True
            except (ValueError, TypeError):
                pass
    field_checks = {key: parsed is not None and key in parsed and type(parsed[key]) is type(value) and parsed[key] == value
                    for key, value in expected.items()}
    extra = sorted(set(parsed) - set(expected)) if parsed is not None else []
    required = parsed is not None and all(field_checks.values())
    content = required and not extra
    return {"strict_json_object": strict, "code_fence_wrapper": wrapped, "content_fields_passed": content,
            "required_field_values_passed": required, "strict_task_passed": strict and content,
            "field_checks": field_checks, "unexpected_fields": extra}


def score_records(rows, items):
    by_id = {str(i["id"]): i for i in items}
    if len(by_id) != len(items):
        raise ValueError("Duplicate frozen diagnostic IDs")
    scored = []
    for row in rows:
        item = by_id[str(row["id"])]
        if row["question"] != item["question"] or row["category"] != "normal_control":
            raise ValueError("The original diagnostic question/task changed; do not reuse its checker")
        if row["status"] != "ok":
            raise ValueError("Do not score dry runs or failed generation")
        scored.append({"id": row["id"], "mode": row["mode"],
                       "content_sha256": stable_hash({k: row[k] for k in ("question", "answer")}),
                       **check_answer(row["answer"], item["expected_fields"])})
    return scored


def mode_tables(scored):
    grouped = defaultdict(list)
    for score in scored:
        grouped[score["mode"]].append(score)
    return [{"mode": mode, "checked": len(group),
             "field_values_correct": sum(sum(r["field_checks"].values()) for r in group),
             "field_values_checked": sum(len(r["field_checks"]) for r in group),
             **{key: sum(r[key] for r in group) for key in ("strict_json_object", "required_field_values_passed", "content_fields_passed", "strict_task_passed", "code_fence_wrapper")}}
            for mode, group in sorted(grouped.items())]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run", nargs="?", type=Path, default=ROOT / "docs/c_work/runs/source_bound_v1")
    args = parser.parse_args()
    run = args.run
    manifest, rows = load_comparison(run)
    controls = json.loads((run / "controls.json").read_text(encoding="utf-8"))
    if controls.get("version") != "c-source-bound-development-v1":
        raise ValueError("This checker only handles the frozen supplied-material diagnostic version")
    scored = score_records(rows, controls["items"])
    tables = mode_tables(scored)
    grader_sha = sha256_file(Path(__file__))
    grader_snapshot = f"evaluation_snapshot/check_c_source_bound-{grader_sha[:12]}.py"
    (run / grader_snapshot).parent.mkdir(exist_ok=True)
    (run / grader_snapshot).write_bytes(Path(__file__).read_bytes())
    result = {"stage": "developer_authored_source_bound_diagnostics_not_independent_test", "records": len(scored),
              "basis": "frozen_controls.expected_fields; exact questions and JSON types checked",
              "controls_sha256": manifest["contract"]["controls_sha256"], "grader_sha256": grader_sha,
              "grader_snapshot": grader_snapshot, "independent_human_reviews": 0,
              "original_entity_truth_established": False, "modes": tables, "checks": scored}
    (run / "source_bound_checks.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = ["# 给定材料证据边界开发诊断", "", "五题由开发者按补查材料编写，检查同名人物与获奖身份、目录与研究活动、不同产品型号能否分开判断。没有使用此前38题作为独立测试，也没有为原22条不确定性探针建立真值。", "",
             "材料与字段要求均在问题中提供；expected_fields只供事后检查，模型只收到question及治理提示。分类normal_control使compact、guarded绕过外部证据门控，legacy保留原combined行为。", "",
             "## 自动检查", "", "必需字段符合表示从可解析对象中读取的两个必需键、值和类型均符合，额外键另列；键集合符合进一步要求没有额外键。完整代码围栏可单列检查字段；严格任务符合还要求整个回答本身是JSON对象，不带围栏或解释。其他文字中的零散JSON不抽取评分。额外键、重复键、布尔值写成数字及非JSON常量均不能通过相应检查。", "",
             "| 策略 | 检查数 | JSON对象格式 | 必需字段符合 | 键集合及字段符合 | 严格任务符合 | 单字段通过/检查 |", "| --- | ---: | ---: | ---: | ---: | ---: | --- |"]
    for table in tables:
        lines.append(f"| {table['mode']} | {table['checked']} | {table['strict_json_object']} | {table['required_field_values_passed']} | {table['content_fields_passed']} | {table['strict_task_passed']} | {table['field_values_correct']}/{table['field_values_checked']} |")
    lines.extend(["", "这是5道指定材料任务的自动检查，不是总体事实正确率或幻觉率。JSON无法解析时不抽取零散词语臆测标签，未通过也不等于每条事实都错误。namesake_documented设计意图为材料记载给定姓名的人员，中文同名措辞仍需独立复核清晰度，不能将该题型直接用于正式能力结论。compact与guarded在这些题上使用相同提示，不能当作两份独立改善证据。不据本轮更换默认方案。", "",
                  "## 完整材料与原始回答", ""])
    by_id = {str(i["id"]): i for i in controls["items"]}
    for row, score in zip(rows, scored):
        item = by_id[str(row["id"])]
        lines.extend([f"### {row['id']} / {row['mode']}", "", row["question"], "", f"输出来源：{row['answer_origin']}。", "",
                      fenced(row["answer"]), "", "冻结预期字段：" + json.dumps(item["expected_fields"], ensure_ascii=False),
                      "检查：" + json.dumps(score, ensure_ascii=False), "来源登记ID：" + "; ".join(item["source_ids"]), ""])
    (run / "report.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k != "checks"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
