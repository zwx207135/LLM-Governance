"""Report candidate behavior, costs and scoped developer observations without declaring a winner."""
import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from experiments.check_c_controls import CHECKED_IDS, check
from experiments.report_c_suite import fenced
from src.utils.experiment_io import latest_records, read_records, sha256_file, stable_hash


def load_comparison(run):
    manifest = json.loads((run / "manifest.json").read_text(encoding="utf-8"))
    if manifest["status"] != "completed" or manifest["contract"]["dry_run"]:
        raise ValueError("Complete the real candidate run first")
    contract = manifest["contract"]
    if stable_hash(contract) != manifest["contract_sha256"]:
        raise ValueError("Modified comparison contract")
    for name in ("dataset", "controls", "corpus"):
        if sha256_file(run / f"{name}.json") != contract[f"{name}_sha256"]:
            raise ValueError(f"Modified {name} snapshot")
    rows = list(latest_records(read_records(run / "records.jsonl")).values())
    if set((str(r["id"]), r["mode"]) for r in rows) != set(map(tuple, manifest["planned_records"])):
        raise ValueError("Missing comparison records")
    if any(r["status"] != "ok" for r in rows):
        raise ValueError("Comparison contains unsuccessful records")
    return manifest, rows


def eligible_controls(rows, frozen, canonical):
    expected = {str(r["id"]): r["question"] for r in canonical["items"]}
    frozen_questions = {str(r["id"]): r["question"] for r in frozen["items"]}
    return [r for r in rows if str(r["id"]) in CHECKED_IDS and r["category"] == "normal_control"
            and r["question"] == frozen_questions.get(str(r["id"])) == expected.get(str(r["id"]))]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run", nargs="?", type=Path, default=ROOT / "docs/c_work/runs/policy_comparison_v1")
    args = parser.parse_args()
    run = args.run
    manifest, rows = load_comparison(run)
    historical = run.resolve() == (ROOT / "docs/c_work/runs/policy_comparison_v1").resolve()
    frozen_controls = json.loads((run / "controls.json").read_text(encoding="utf-8"))
    canonical_controls = json.loads((ROOT / "datasets/controls/c_normal_development.json").read_text(encoding="utf-8"))
    policies = manifest["contract"]["config"]["policies"]
    tables = []
    for domain in ("development", "normal_controls"):
        for policy in policies:
            part = [r for r in rows if r["mode"] == policy and (r["category"] == "normal_control") == (domain == "normal_controls")]
            called = [r for r in part if r["model_calls"]]
            formats = eligible_controls(part, frozen_controls, canonical_controls)
            tables.append({"domain": domain, "policy": policy, "records": len(part),
                           "model_calls": sum(r["model_calls"] for r in part),
                           "policy_abstentions": sum(r["answer_origin"] == "policy_abstention" for r in part),
                           "guard_reasons": dict(Counter(r["guard_reason"] for r in part if r["guard_reason"])),
                           "mean_generation_seconds_model_calls_only": round(mean(r["generation_seconds"] for r in called), 4) if called else None,
                           "mean_prepare_plus_generation_seconds": round(mean(r["generation_seconds"] + r["prepare_seconds"] for r in part), 4),
                           "mean_model_output_tokens_calls_only": round(mean(r["output_tokens"] for r in called), 2) if called else None,
                           "truncated": sum(r["truncated"] for r in part),
                           "closed_constraints_passed": sum(check(str(r["id"]), r["answer"]) for r in formats),
                           "closed_constraints_checked": len(formats)})
    original = {}
    for name in ("expanded_v3", "controls_v3"):
        original.update({key: value for key, value in latest_records(read_records(ROOT / "docs/c_work/runs" / name / "records.jsonl")).items() if key[1] == "combined"})
    replay = [r for r in rows if r["mode"] == "legacy"]
    comparable = [r for r in replay if (str(r["id"]), "combined") in original
                  and r["question"] == original[(str(r["id"]), "combined")]["question"]]
    same_prompt = sum(r["prompt"] == original[(str(r["id"]), "combined")]["prompt"] for r in comparable)
    same_answer = sum(r["answer"] == original[(str(r["id"]), "combined")]["answer"] for r in comparable)
    result = {"stage": "development_selection_not_final_test", "records": len(rows),
              "model_generated_answers": sum(r["model_calls"] for r in rows),
              "program_abstentions": sum(r["answer_origin"] == "policy_abstention" for r in rows),
              "legacy_replay": {"n": len(comparable), "unmatched": len(replay) - len(comparable), "same_prompt": same_prompt, "same_answer": same_answer}, "tables": tables,
              "independent_human_reviews": 0, "formal_winner_selected": False}
    (run / "summary.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    metrics = {"tables": []}
    if historical:
        from experiments.evaluate_c_reviews import load_and_validate
        from src.evaluation.review_metrics import summarize
        metrics = summarize(load_and_validate([ROOT / "docs/c_work/reviews/developer_reviews_v1.json"]), include_ai=True)
    n_development = len({str(r["id"]) for r in rows if r["category"] != "normal_control"})
    n_controls = len({str(r["id"]) for r in rows if r["category"] == "normal_control"})
    lines = ["# 证据提示与保守门控开发比较", "",
             f"{n_development}道开发题与{n_controls}道正常任务，共{len(policies)}组，得到{len(rows)}条输出；其中{result['model_generated_answers']}条模型生成，{result['program_abstentions']}条程序拒答。样本、生成设置与预先指定复核题见冻结config.json。此报告不自动生成事实正确性标签。", "",
             "legacy保留原combined提示；compact缩短规则并将来源URL保留在日志，提示中只显示资料编号；guarded在compact基础上遇到无资料或引号主体未在资料出现时返回限定说明。数学与正常操作任务绕过外部证据门控。门控不读取参考答案、数据用途标签或评分。", "",
             "## 输出来源与成本", "", "| 范围 | 策略 | 记录 | 模型调用 | 程序拒答 | 模型调用平均生成秒 | 截断 |", "| --- | --- | ---: | ---: | ---: | ---: | ---: |"]
    for r in tables:
        lines.append(f"| {r['domain']} | {r['policy']} | {r['records']} | {r['model_calls']} | {r['policy_abstentions']} | {r['mean_generation_seconds_model_calls_only']} | {r['truncated']} |")
    lines.extend(["", "程序模板不计为模型生成token或模型调用。准备加生成耗时另存，不能把跳过调用造成的低耗时当成模型效率改善。", "",
                  f"legacy中{len(comparable)}条可按ID和同一问题与旧combined对照，prompt逐字相同{same_prompt}条，回答逐字相同{same_answer}条；另有{len(replay)-len(comparable)}条未匹配。重复输出不是新增独立标注。", ""])
    if historical:
        lines.extend([
                  "## 单一AI开发者的12例复核", "", "以下是刻意选择的失败与边界案例，尚未经过独立人工评分，不能外推为总体效果。两条未知实体题不计算核心正确分母。", "",
                  "| 策略 | 核心正确 | 已判定含错误事实 | 事实未核实或不适用 | 不恰当拒答 |", "| --- | ---: | ---: | ---: | ---: |"])
    for r in metrics["tables"]:
        if r["run"] == "policy_comparison_v1":
            lines.append(f"| {r['mode']} | {r['core_correct_numerator']}/{r['core_correct_denominator']} | {r['factual_error_numerator']}/{r['factual_error_denominator']} | {r['factual_unverifiable_or_na']} | {r['refusal'].get('inappropriate', 0)} |")
    if historical:
        lines.extend(["", "compact在牛顿相对论归因与电灯归因等案例有所改善，但瓦特题只给1712年，仍把正确数字错配给题设主体；太阳题仍有自相矛盾。产品探针中还编造了10万元售价。", "",
                  "guarded阻止了若干无证据陈述，但也拒答首都北京这一有明确答案的题目。它返回的是程序模板，不可表述为模型自己学会了核验。引号主体匹配也可能错拒别名或同义表达。", "",
                  ])
    else:
        lines.extend(["当前目录未关联经哈希核验的事实评分，不沿用其他运行的AI开发判断或案例结论。", ""])
    lines.extend(["## 正常任务代价", "", "| 策略 | 封闭任务输出约束符合 |", "| --- | ---: |"])
    for r in tables:
        if r["domain"] == "normal_controls":
            lines.append(f"| {r['policy']} | {r['closed_constraints_passed']}/{r['closed_constraints_checked']} |")
    lines.extend(["", "compact与guarded在正常操作任务上采用相同路由与提示，因此其重复输出不构成两份独立改善证据。封闭检查仅按冻结controls.json中与原始任务完全相同的六题规则核验，不能代替整体任务质量。", "",
                  "当前保留三组作为开发候选，不替换正式方案。下一步由独立复核及更广的开发资料覆盖决定取舍，不用单一加权总分掩盖拒答和能力代价。", "",
                  "## 原始回答", ""])
    for ident in dict.fromkeys(str(r["id"]) for r in rows):
        group = [r for r in rows if str(r["id"]) == str(ident)]
        lines.extend([f"### {ident}", "", group[0]["question"], ""])
        for policy in policies:
            row = next(r for r in group if r["mode"] == policy)
            lines.extend([f"{policy}；输出来源：{row['answer_origin']}；门控原因：{row['guard_reason']}。", "", fenced(row["answer"]), ""])
    (run / "report.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
