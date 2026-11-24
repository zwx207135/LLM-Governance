"""Trace old failures and report paired diagnostics without inventing accuracy labels."""
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.governance.retrieval import LocalRetriever
from src.governance.retrieval_safe import SafeAnchorRetriever
from src.governance.anti_hallucination import AntiHallucination
from src.utils.experiment_io import sha256_file, stable_hash

DIAGNOSES = {
    1: ("coverage_gap_control", "库中无首都资料，但旧回答北京正确；无命中不能自动判错误或拒答。"),
    7: ("coverage_gap_and_anchor_collision", "相对论片段不证明获奖次数；贝尔由诺贝尔子串误入；回答先否认获奖又声称1921年获奖。"),
    17: ("entity_hierarchy_error", "已召回海沟与内部深渊关系，回答却把挑战者深渊当作海沟。"),
    18: ("supported_answer_control", "已有声波需要介质的直接证据，旧回答正确表达不能在真空传播。"),
    28: ("subject_binding_and_identity_gap", "通用相对论资料没有题设人物身份或贡献证据；回答把他人贡献移植到该姓名。不能据此判定同名人物不存在。"),
    32: ("no_hit_abstention_control", "无产品资料，旧回答说明无法提供参数；不把缺资料变为公司或产品不存在的真值。"),
    38: ("source_not_ingested", "题目指定年报没有进入当轮RAG，回答仍声称年报列出或未列出内容。问题来源登记不等于推理时已得到原文。"),
    76: ("premise_correction_failure", "狭义相对论片段明确爱因斯坦，模型仍把广义相对论归给牛顿；不能把此例简单归为无资料。"),
    84: ("evidence_ignored", "首条资料已说明纽科门早于瓦特且瓦特是改进者，回答仍承认瓦特最初发明并编造时间关系。"),
    94: ("task_incomplete", "只输出真实来源链接，没有回答或纠正题目前提；链接真实性不能替代任务完成。"),
    99: ("contradiction_and_category_error", "资料说明太阳是唯一恒星且不是行星，回答仍先说唯一、再说有其他恒星并列行星。"),
}


def load_run(name):
    folder = ROOT / "docs/c_work/runs" / name
    manifest = json.loads((folder / "manifest.json").read_text(encoding="utf-8"))
    if manifest["status"] != "completed" or manifest["counts"] != {"planned": 32, "ok": 32, "prepared": 0, "errors": 0, "missing": 0}:
        raise ValueError("Incomplete diagnostic run")
    if stable_hash(manifest["contract"]) != manifest["contract_sha256"]:
        raise ValueError("Contract hash mismatch")
    contract = manifest["contract"]
    for name, key in [("dataset.json", "dataset_sha256"), ("corpus.json", "corpus_sha256")]:
        if sha256_file(folder / name) != contract[key]:
            raise ValueError("Input snapshot mismatch")
    for relative, expected in contract["runtime_sha256"].items():
        if sha256_file(folder / "source_snapshot" / relative) != expected:
            raise ValueError("Code snapshot mismatch")
    records = [json.loads(line) for line in (folder / "records.jsonl").read_text(encoding="utf-8").splitlines()]
    by_key = {(str(r["id"]), r["mode"]): r for r in records}
    if len(records) != 32 or len(by_key) != 32 or any(r["status"] != "ok" or r.get("model_calls") != 1 for r in records):
        raise ValueError("Unexpected diagnostic records")
    if set(by_key) != {tuple(x) for x in manifest["planned_records"]}:
        raise ValueError("Record identity differs from plan")
    config = contract["config"]
    stored_config = json.loads((folder / "config.json").read_text(encoding="utf-8"))
    if {k: v for k, v in config.items() if k != "prompt_policy"} != stored_config:
        raise ValueError("Effective configuration differs from original snapshot")
    dataset = json.loads((folder / "dataset.json").read_text(encoding="utf-8"))["items"]
    items = {str(x["id"]): x for x in dataset if x["id"] in config["existing_ids"]}
    items.update({str(x["id"]): x for x in config["probes"]})
    retrievers = {"legacy": LocalRetriever(folder / "corpus.json"), "safe_anchor": SafeAnchorRetriever(folder / "corpus.json")}
    for (ident, mode), row in by_key.items():
        item = items[ident]
        if (row["question"], row["category"]) != (item["question"], item["category"]):
            raise ValueError("Question differs from frozen input")
        prepared = AntiHallucination(retrievers[mode], **config["retrieval"]).prepare(item["question"], "combined", item["category"])
        scaffold = config.get("prompt_policy", "original_combined")
        if scaffold != "original_combined" and prepared["evidence"]:
            prepared["prompt"] = scaffold + "\n\n" + prepared["prompt"]
        if any(row[k] != prepared[k] for k in ("prompt", "evidence", "retrieval_status")):
            raise ValueError("Prompt/evidence differs from question-only preparation")
    return folder, manifest, by_key


def main():
    out = ROOT / "docs/c_work"
    source = out / "runs/expanded_v3/records.jsonl"
    ledger = []
    for n, line in enumerate(source.read_text(encoding="utf-8").splitlines(), 1):
        row = json.loads(line)
        if row["id"] in DIAGNOSES and row["mode"] == "combined":
            diagnosis, rationale = DIAGNOSES[row["id"]]
            ledger.append({"id": row["id"], "diagnosis": diagnosis, "rationale": rationale,
                           "review_origin": "AI_developer_diagnostic_not_independent_human_label",
                           "source_file": str(source.relative_to(ROOT)), "source_file_sha256": sha256_file(source),
                           "source_line": n, "record_semantic_sha256": stable_hash(row), "raw_record": row})
    if len(ledger) != len(DIAGNOSES):
        raise ValueError("Historical case missing")
    (out / "failure_evidence_ledger_v1.json").write_text(json.dumps({"stage": "development_only", "cases": ledger}, ensure_ascii=False, indent=2), encoding="utf-8")
    runs = {name: load_run(name) for name in ("anchor_diagnostics_v1", "evidence_first_v1")}
    first = runs["anchor_diagnostics_v1"][1]["contract"]
    second = runs["evidence_first_v1"][1]["contract"]
    for key in ("dataset_sha256", "corpus_sha256", "model_sha256"):
        if first[key] != second[key]:
            raise ValueError("Paired run inputs differ: " + key)
    for key in ("existing_ids", "probes", "generation", "seed", "retrieval"):
        if first["config"][key] != second["config"][key]:
            raise ValueError("Paired run setting differs: " + key)
    summaries, comparisons = {}, []
    for name, (_, manifest, rows) in runs.items():
        ids = [ident for ident, mode in rows if mode == "legacy"]
        comparisons.extend({"run": name, "id": ident, "legacy": rows[ident, "legacy"], "safe_anchor": rows[ident, "safe_anchor"]} for ident in ids)
        summaries[name] = {"model_calls": len(rows), "pairs": len(ids),
                           "changed_prompts": sum(rows[i, "legacy"]["prompt"] != rows[i, "safe_anchor"]["prompt"] for i in ids),
                           "changed_answers": sum(rows[i, "legacy"]["answer"] != rows[i, "safe_anchor"]["answer"] for i in ids),
                           "truncated_outputs": sum(r["truncated"] for r in rows.values()),
                           "rejected_candidates": sum(len(r.get("rejected", [])) for r in rows.values()),
                           "factual_accuracy": None, "human_review_count": 0,
                           "records_sha256": sha256_file(runs[name][0] / "records.jsonl")}
    corpus = ROOT / "knowledge/corpus_v3.json"
    old, new = LocalRetriever(corpus), SafeAnchorRetriever(corpus)
    all_items = json.loads((ROOT / "datasets/hallucination/test_set.json").read_text(encoding="utf-8"))["items"]
    # Retrieval-only regression over already exposed data, not new held-out truth.
    changes = []
    for item in all_items:
        before, after = old.search(item["question"]), new.search(item["question"])
        if before != after:
            changes.append({"id": item["id"], "question": item["question"], "before": [h["id"] for h in before],
                            "after": [h["id"] for h in after], "diagnostics": new.search_with_diagnostics(item["question"])["rejected"]})
    summary = {"stage": "targeted_development_diagnostics", "runs": summaries, "historical_cases": len(ledger),
               "historical_diagnosis_counts": dict(Counter(x["diagnosis"] for x in ledger)),
               "retrieval_only_checked_questions": len(all_items), "retrieval_changes": changes,
               "factual_accuracy": None, "human_review_count": 0}
    (out / "anchor_diagnostics_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    (out / "anchor_diagnostics_comparison.json").write_text(json.dumps(comparisons, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
