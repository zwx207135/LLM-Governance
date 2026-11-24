"""Verify joint batch provenance and report operational/closed-format results separately."""
import argparse
import json
from collections import Counter
from pathlib import Path
from statistics import mean
from experiments.check_c_source_bound import parse_object
from experiments.report_c_suite import fenced
from src.governance.consistency_v2 import check_consistency_v2
from src.utils.experiment_io import latest_records, read_records, sha256_file, stable_hash

ROOT = Path(__file__).resolve().parents[1]


def closed_check(ident, answer):
    if ident not in ("N1", "N2", "N3", "N4"):
        return None
    if ident != "N3":
        return answer.strip() == {"N1": "林青", "N2": "3,5,8", "N4": "HELLO"}[ident]
    try:
        obj = parse_object(answer.strip())
        return set(obj) == {"name", "age"} and obj["name"] == "林青" and type(obj["age"]) is int and obj["age"] == 23
    except ValueError:
        return False


def analyze(run):
    manifest = json.loads((run / "manifest.json").read_text(encoding="utf-8"))
    c = manifest["contract"]
    if manifest["status"] != "completed" or c["dry_run"] or stable_hash(c) != manifest["contract_sha256"]:
        raise ValueError("Completed real batch with unchanged contract required")
    for name in ("dataset", "corpus"):
        if sha256_file(run / (name + ".json")) != c[name + "_sha256"]:
            raise ValueError("Input snapshot changed")
    for name, digest in c["runtime_sha256"].items():
        if sha256_file(run / "source_snapshot" / name) != digest:
            raise ValueError("Runtime snapshot changed")
    rows = latest_records(read_records(run / "records.jsonl"))
    if set(rows) != set(map(tuple, manifest["planned_records"])):
        raise ValueError("Missing/extra records")
    items = {str(i["id"]): i for i in json.loads((run / "dataset.json").read_text(encoding="utf-8"))["items"]}
    conditions = {i["name"]: i for i in c["config"]["conditions"]}
    for (ident, mode), row in rows.items():
        item = items[ident]
        if row["status"] != "ok" or row["question"] != item["question"] or row["strategy"] != conditions[mode]["strategy"] or row["bias_mode"] != conditions[mode]["bias_mode"]:
            raise ValueError("Failed or mismatched joint record")
        if item["question"] not in row["effective_question"] or row["supplied_materials"] != item.get("materials", []):
            raise ValueError("Wrong material/question context")
        if row["consistency_v2"] != check_consistency_v2(row["answer"], row["evidence"], row["evidence_labels"], row["supplied_materials"]):
            raise ValueError("Audit differs from raw response")
        if row["answer_origin"] == "model":
            if row["model_calls"] != 1 or sha256_file_bytes(row["final_prompt"]) != row["final_prompt_sha256"]:
                raise ValueError("Model provenance mismatch")
            if any(m["text"] not in row["final_prompt"] for m in row["supplied_materials"]):
                raise ValueError("Materials missing from actual model prompt")
        elif row["answer_origin"] != "policy_abstention" or row["model_calls"] != 0:
            raise ValueError("Program/model origins mixed")
    tables = []
    for mode in conditions:
        part = [r for r in rows.values() if r["mode"] == mode]
        signals = Counter(f["code"] for r in part for f in r["consistency_v2"]["flags"])
        normal = [closed_check(str(r["id"]), r["answer"]) for r in part if str(r["id"]) in ("N1", "N2", "N3", "N4")]
        pairs = {}
        for r in part:
            if r.get("pair_id"):
                pairs.setdefault(r["pair_id"], []).append(r)
        tables.append({"mode": mode, "records": len(part), "model_answers": sum(r["model_calls"] for r in part),
                       "program_abstentions": sum(r["answer_origin"] == "policy_abstention" for r in part),
                       "flagged_records": sum(bool(r["consistency_v2"]["flags"]) for r in part), "signals": dict(signals),
                       "normal_constraints_passed": sum(normal), "normal_constraints_checked": len(normal),
                       "literal_pair_same_answer": sum(len(v) == 2 and v[0]["answer"] == v[1]["answer"] for v in pairs.values()),
                       "literal_pairs": len(pairs), "mean_request_seconds": round(mean(r["request_seconds"] for r in part), 4)})
    summary = {"stage": "joint_development_integration_not_E3_effectiveness", "records": len(rows),
               "model_generated_answers": sum(r["model_calls"] for r in rows.values()),
               "program_abstentions": sum(r["answer_origin"] == "policy_abstention" for r in rows.values()),
               "independent_human_reviews": 0, "bias_effectiveness": "not_evaluated", "semantic_support": "not_evaluated", "modes": tables}
    return summary, list(rows.values())


def sha256_file_bytes(text):
    import hashlib
    return hashlib.sha256(text.encode()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run", nargs="?", type=Path, default=ROOT / "docs/c_work/runs/joint_batch_v1")
    args = parser.parse_args()
    summary, rows = analyze(args.run)
    (args.run / "joint_checks.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = ["# 联合入口批量集成对照", "", "24个开发案例、4条件，共96条输出。偏见属性包含6个配对，其中3组属性正反顺序重复，不作为12个独立偏见案例。其余为事实、未知实体、数学、材料与格式任务。", "",
             "原偏见模块尚未提供，本轮使用显式偏见约束提示；只验证集成行为，不宣称E3效果。程序拒答、模型回答及审计信号分开报告。", "",
             "| 条件 | 输出 | 模型回答 | 程序拒答 | 触发审计 | 四项严格任务符合 |", "| --- | ---: | ---: | ---: | ---: | ---: |"]
    for t in summary["modes"]:
        lines.append(f"| {t['mode']} | {t['records']} | {t['model_answers']} | {t['program_abstentions']} | {t['flagged_records']} | {t['normal_constraints_passed']}/{t['normal_constraints_checked']} |")
    lines.extend(["", "更多程序拒答不表示效果更好，未触发审计不表示事实正确。四项严格任务仅检查明确提取、排序、JSON与大小写要求，不代替偏见或事实评分。逐字配对相同数仅作集成观察，相同回答可能是固定拒答，不能当作公平性。端到端请求耗时包括策略与审计，不能直接与旧纯生成时延比较。", "",
                  "## 原始回答", ""])
    for row in rows:
        lines.extend([f"### {row['id']} / {row['mode']}", "", row["effective_question"], "", f"来源：{row['answer_origin']}。", fenced(row["answer"]),
                      "审计：" + json.dumps(row["consistency_v2"], ensure_ascii=False), ""])
    (args.run / "report.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
