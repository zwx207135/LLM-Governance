"""Diagnose original failures and compare explicit normal-task routes without selecting a winner."""
import json
from pathlib import Path
from experiments.report_c_joint_batch import analyze, closed_check
from experiments.check_c_controls import CHECKED_IDS, check
from src.utils.experiment_io import latest_records, read_records

ROOT = Path(__file__).resolve().parents[1]


def main():
    run = ROOT / "docs/c_work/runs/normal_route_v1"
    base, rows = analyze(run)
    old = latest_records(read_records(ROOT / "docs/c_work/runs/joint_batch_v1/records.jsonl"))
    canonical = {str(i["id"]): i["question"] for i in json.loads((ROOT / "datasets/controls/c_normal_development.json").read_text(encoding="utf-8"))["items"]}
    cases = []
    for r in rows:
        ident = str(r["id"])
        passed = closed_check(ident, r["answer"])
        if ident in CHECKED_IDS:
            if r["question"] != canonical[ident]:
                raise ValueError("Do not reuse a checker after changing the question")
            passed = check(ident, r["answer"])
        if passed is not None:
            cases.append({"id": ident, "mode": r["mode"], "passed": bool(passed), "answer": r["answer"]})
    tables = [{"mode": m, "passed": sum(c["passed"] for c in cases if c["mode"] == m),
               "checked": sum(c["mode"] == m for c in cases)} for m in ("combined_prompt", "baseline_off")]
    replays = [r for r in rows if r["mode"] == "combined_prompt" and r["id"] in ("N1", "N2", "N3", "N4")]
    result = {"stage": "normal_task_development_route_comparison", "records": len(rows), "model_generated_answers": base["model_generated_answers"],
              "strict_checks": tables, "original_combined_prompt_replay": {"n": len(replays), "same_answer": sum(r["answer"] == old[(r["id"], "combined_prompt")]["answer"] for r in replays)},
              "formal_winner_selected": False, "independent_human_reviews": 0, "checks": cases}
    (run / "normal_route_checks.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = ["# 正常任务退化定位与扩展对照", "",
             "原四题中，compact/guarded比combined少通过的一题是JSON外围增加代码围栏，姓名和年龄字段内容正确。大写题四组均失败：combined输出H ello，compact/guarded输出HOLLO。这四题没有程序拒答，不能将本次差异解释为拒答策略造成。", "",
             "本轮复用原四题与已有20条正常任务，共24题两条件48条真实模型输出。combined_prompt保留联合提示；baseline_off直接使用问题。该整体路由对照同时改变多项提示，不能单独归因于某一句偏见规则或事实约束。", "",
             "十道封闭任务按已有规则检查，其余十四道开放任务仅保留原件，不自动评分。数据均为既有开发任务，不是独立测试。", "",
             "| 路由 | 指定输出约束符合 |", "| --- | ---: |"]
    for t in tables:
        lines.append(f"| {t['mode']} | {t['passed']}/{t['checked']} |")
    lines.extend(["", "原四题中baseline_off为4/4，combined_prompt为3/4；扩展六题中baseline_off为1/6，combined_prompt为2/6，合计均为5/10。因此简化提示能修好大写例子，却不能证明整体更优，当前不改默认路由。其余14条开放任务未自动判分。", "",
                  "原combined_prompt四条全部逐字重放一致。原始回答、输入和源码快照保留。", "", "## 全部原始回答", ""])
    from experiments.report_c_suite import fenced
    for r in rows:
        lines.extend([f"### {r['id']} / {r['mode']}", "", r["question"], "", fenced(r["answer"]), ""])
    (run / "report.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k != "checks"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
