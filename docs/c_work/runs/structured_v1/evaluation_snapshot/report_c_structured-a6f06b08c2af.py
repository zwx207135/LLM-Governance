"""Verify and report format constraints separately from supplied-material field correctness."""
import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from experiments.check_c_source_bound import check_answer, parse_object
from experiments.report_c_suite import fenced
from experiments.run_c_structured_comparison import generation_tasks
from src.governance.evidence_policy import EvidencePolicy
from src.governance.retrieval import LocalRetriever
from src.utils.experiment_io import latest_records, read_records, sha256_file, stable_hash


def schema_conformant(answer, schema):
    try:
        value = parse_object(answer.strip())
    except (ValueError, TypeError):
        return False
    fields = schema["fields"]
    return set(value) == {f["name"] for f in fields} and all(
        any(type(value[f["name"]]) is type(v) and value[f["name"]] == v for v in f["values"]) for f in fields)


def analyze(run):
    manifest = json.loads((run / "manifest.json").read_text(encoding="utf-8"))
    contract = manifest["contract"]
    if manifest["status"] != "completed" or contract["dry_run"] or stable_hash(contract) != manifest["contract_sha256"]:
        raise ValueError("A complete real run with an unchanged contract is required")
    for name in ("controls", "schemas", "corpus"):
        if sha256_file(run / (name + ".json")) != contract[name + "_sha256"]:
            raise ValueError("Modified structured comparison input")
    for name, expected in contract["runtime_sha256"].items():
        if sha256_file(run / "source_snapshot" / name) != expected:
            raise ValueError("Modified structured generation source snapshot")
    controls = json.loads((run / "controls.json").read_text(encoding="utf-8"))
    schemas = json.loads((run / "schemas.json").read_text(encoding="utf-8"))["schemas"]
    tasks, outputs = generation_tasks(controls, schemas)
    gold = {str(i["id"]): i["expected_fields"] for i in controls["items"]}
    questions = {str(t["id"]): t["question"] for t in tasks}
    latest = latest_records(read_records(run / "records.jsonl"))
    if set(latest) != set(map(tuple, manifest["planned_records"])):
        raise ValueError("Missing or extra structured answers")
    rows = list(latest.values())
    governance = EvidencePolicy(LocalRetriever(run / "corpus.json"), **contract["config"]["retrieval"])
    checked = []
    for row in rows:
        ident = str(row["id"])
        if row["status"] != "ok" or row["answer_origin"] != "model" or row["model_calls"] != 1:
            raise ValueError("All comparison outputs must be actual model answers")
        if row["mode"] != row["policy"] + "__" + row["decoder"] or row["question"] != questions[ident] or row["category"] != "normal_control":
            raise ValueError("Question, task or decoder identity mismatch")
        if row["prompt"] != governance.prepare(row["question"], row["policy"], row["category"])["prompt"]:
            raise ValueError("Prompt changed or received grading metadata")
        if row["decoder"] == "json":
            if row["allowed_outputs"] != outputs[ident] or row["allowed_outputs_sha256"] != stable_hash(outputs[ident]):
                raise ValueError("Constraint filtered or changed the declared semantic combinations")
            if row["answer"] not in outputs[ident] or row["truncated"]:
                raise ValueError("Constrained output did not complete a schema-permitted object")
        elif row["decoder"] != "free" or row["allowed_outputs"] or row["allowed_outputs_sha256"] is not None:
            raise ValueError("Free generation must not use an answer whitelist")
        checked.append({"id": row["id"], "policy": row["policy"], "decoder": row["decoder"], "mode": row["mode"],
                        "content_sha256": stable_hash({k: row[k] for k in ("question", "answer")}),
                        "schema_conformant": schema_conformant(row["answer"], schemas[ident]),
                        **check_answer(row["answer"], gold[ident])})
    grouped = defaultdict(list)
    for row, score in zip(rows, checked):
        grouped[(row["policy"], row["decoder"])].append((row, score))
    tables = []
    for (policy, decoder), group in sorted(grouped.items()):
        tables.append({"policy": policy, "decoder": decoder, "records": len(group),
                       "json_objects": sum(s["strict_json_object"] for r, s in group),
                       "schema_conformant": sum(s["schema_conformant"] for r, s in group),
                       "required_field_values_passed": sum(s["required_field_values_passed"] for r, s in group),
                       "strict_task_passed": sum(s["strict_task_passed"] for r, s in group),
                       "field_values_correct": sum(sum(s["field_checks"].values()) for r, s in group),
                       "field_values_checked": sum(len(s["field_checks"]) for r, s in group),
                       "mean_generation_seconds": round(mean(r["generation_seconds"] for r, s in group), 4),
                       "mean_constraint_compile_seconds": round(mean(r["constraint_compile_seconds"] for r, s in group), 4),
                       "mean_total_seconds": round(mean(r["prepare_seconds"] + r["constraint_compile_seconds"] + r["generation_seconds"] for r, s in group), 4),
                       "mean_output_tokens": round(mean(r["output_tokens"] for r, s in group), 2)})
    lookup = {(str(r["id"]), r["policy"], r["decoder"]): (r, s) for r, s in zip(rows, checked)}
    paired = []
    for policy in contract["config"]["policies"]:
        group = [(lookup[(str(t["id"]), policy, "free")], lookup[(str(t["id"]), policy, "json")]) for t in tasks]
        if any(a[0]["prompt"] != b[0]["prompt"] for a, b in group):
            raise ValueError("A decoder comparison must use identical prompts")
        paired.append({"policy": policy, "paired_questions": len(group), "identical_prompts": len(group),
                       "both_parseable_objects": sum((a[1]["strict_json_object"] or a[1]["code_fence_wrapper"]) and
                                                       (b[1]["strict_json_object"] or b[1]["code_fence_wrapper"]) for a, b in group),
                       "strict_task_gains": sum(not a[1]["strict_task_passed"] and b[1]["strict_task_passed"] for a, b in group),
                       "strict_task_losses": sum(a[1]["strict_task_passed"] and not b[1]["strict_task_passed"] for a, b in group)})
    old_run = ROOT / "docs/c_work/runs/source_bound_v1"
    old_manifest = json.loads((old_run / "manifest.json").read_text(encoding="utf-8"))
    old = latest_records(read_records(old_run / "records.jsonl"))
    free = [r for r in rows if r["decoder"] == "free"]
    matched = [r for r in free if (str(r["id"]), r["policy"]) in old and r["question"] == old[(str(r["id"]), r["policy"])]["question"]]
    replay = {"matched": len(matched), "unmatched": len(free) - len(matched),
              "same_prompt": sum(r["prompt"] == old[(str(r["id"]), r["policy"])]["prompt"] for r in matched),
              "same_answer": sum(r["answer"] == old[(str(r["id"]), r["policy"])]["answer"] for r in matched),
              "same_model_files": contract["model_sha256"] == old_manifest["contract"]["model_sha256"]}
    result = {"stage": contract["config"]["stage"], "records": len(rows), "model_generated_answers": len(rows),
              "program_abstentions": 0, "independent_human_reviews": 0, "formal_winner_selected": False,
              "all_declared_combinations_per_task": {i: len(v) for i, v in outputs.items()},
              "gold_fields_used_for_generation": False, "free_replay": replay, "modes": tables, "paired": paired, "checks": checked,
              "warning": "Finite-format control is mechanical. Supplied-material diagnostics and wording remain developer-authored, not independent factual evaluation."}
    return result, rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run", nargs="?", type=Path, default=ROOT / "docs/c_work/runs/structured_v1")
    args = parser.parse_args()
    result, rows = analyze(args.run)
    sources = ("experiments/report_c_structured.py", "experiments/check_c_source_bound.py")
    result["evaluation_sources"] = {}
    for name in sources:
        digest = sha256_file(ROOT / name)
        relative = f"evaluation_snapshot/{Path(name).stem}-{digest[:12]}.py"
        path = args.run / relative
        path.parent.mkdir(exist_ok=True)
        path.write_bytes((ROOT / name).read_bytes())
        result["evaluation_sources"][relative] = digest
    (args.run / "structured_checks.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = ["# 普通生成与有限JSON约束解码", "", "五道既有给定材料诊断、三种提示策略、两种解码方式，共30条真实模型回答。问题、资料与提示保持一致，只改变下一token可选集合。全部6种语义组合保留，正确字段不参与生成；源码、模式及输入均冻结。", "",
             "## 格式与内容分开报告", "", "| 策略 | 解码 | 数量 | JSON格式 | 字段结构与类型 | 必需值均符合 | 严格任务符合 | 单字段通过/检查 |", "| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |"]
    for r in result["modes"]:
        lines.append(f"| {r['policy']} | {r['decoder']} | {r['records']} | {r['json_objects']} | {r['schema_conformant']} | {r['required_field_values_passed']} | {r['strict_task_passed']} | {r['field_values_correct']}/{r['field_values_checked']} |")
    lines.extend(["", "json解码固定键集合、字段顺序和序列化，禁止代码围栏及额外字段，保留每个布尔值与每个状态值。格式通过是程序约束的结果，不证明模型理解资料或事实更可靠。即使所有结构合格，模型仍可能选错布尔值或证据状态。", "",
                  "必需字段检查允许完整代码围栏内对象另查内容；严格任务要求整个回答本身满足JSON与预期值。无效JSON不靠零散词语强行恢复，因此从普通输出到可解析输出的字段通过变化也包含可检查性的变化，不能一概解释为事实纠错。", "",
                  "人员题同名措辞仍需第二人审核清晰度。本轮保留原题便于隔离解码作用，不将该诊断或其重复提示当作独立测试，不更换默认治理方案。", "",
                  "## 旧输出重放", "", json.dumps(result["free_replay"], ensure_ascii=False), "",
                  "## 耗时与配对", "", "准备、约束编译、生成及输出token分别保存；约束改变输出长度且有回调开销，不据此泛化模型效率提升。", "",
                  "```json", json.dumps({"paired": result["paired"], "costs": [{k: v for k, v in r.items() if k in ("policy", "decoder", "mean_generation_seconds", "mean_constraint_compile_seconds", "mean_total_seconds", "mean_output_tokens")} for r in result["modes"]]}, ensure_ascii=False, indent=2), "```", "",
                  "## 所有原始回答", ""])
    for row in rows:
        lines.extend([f"### {row['id']} / {row['mode']}", "", row["question"], "", fenced(row["answer"]), ""])
    (args.run / "report.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k != "checks"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
