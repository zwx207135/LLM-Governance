"""Validate and publish an append-only follow-up without rewriting frozen development inputs."""
import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.utils.experiment_io import sha256_file

FROZEN = ("datasets/hallucination/test_set.json", "docs/c_work/data_audit.json", "docs/c_work/source_registry.json",
          "docs/c_work/reviewed_candidate.json", "docs/c_work/development_dataset.json", "docs/c_work/data_usage.json", "knowledge/corpus_v3.json")


def validate_followup(payload, audit):
    expected = {r["id"] for r in audit["items"] if r["source_verification_status"] == "pending_source_review"}
    reviews = payload["reviews"]
    if {r["id"] for r in reviews} != expected or len(reviews) != len(expected):
        raise ValueError("Follow-up must cover each original pending ID exactly once")
    sources = {s["id"]: s for s in payload["sources"]}
    if len(sources) != len(payload["sources"]):
        raise ValueError("Duplicate follow-up source IDs")
    for source in sources.values():
        if urlparse(source["url"]).scheme != "https" or not urlparse(source["url"]).netloc:
            raise ValueError("Direct HTTPS source URLs required")
        if source.get("access_method") not in ("direct_body", "indexed_body") or not all(source.get(k) for k in ("locator", "supports", "does_not_support")):
            raise ValueError("Record actual access, scope and limits")
    for review in reviews:
        if review.get("disposition") not in ("reference_issue", "context_only", "pending_source_review"):
            raise ValueError("Do not turn contextual evidence into verified core truth")
        if not review.get("queries") or not review.get("finding") or not review.get("next_step"):
            raise ValueError("Record search attempts, findings and next action")
        if any(s not in sources for s in review["source_ids"]):
            raise ValueError("Unregistered follow-up evidence")
        if review["disposition"] != "pending_source_review" and not review["source_ids"]:
            raise ValueError("Positive or contextual findings require actual source evidence")
        if review["disposition"] == "reference_issue" and not review.get("proposed_reference"):
            raise ValueError("Reference issues need a concrete reviewable proposal")
    if payload.get("reviewer_type") != "ai_developer" or payload.get("independent_human_reviews_completed") != 0:
        raise ValueError("This developer follow-up must not impersonate independent human review")
    return dict(Counter(r["disposition"] for r in reviews))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=ROOT / "docs/c_work/source_followup_v1.json")
    parser.add_argument("--output", type=Path, default=ROOT / "docs/c_work/source_followup_v1")
    args = parser.parse_args()
    payload = json.loads(args.input.read_text(encoding="utf-8"))
    audit = json.loads((ROOT / "docs/c_work/data_audit.json").read_text(encoding="utf-8"))
    counts = validate_followup(payload, audit)
    original = {r["id"]: r for r in audit["items"]}
    frozen = {p: sha256_file(ROOT / p) for p in FROZEN}
    args.output.mkdir(parents=True, exist_ok=False)
    (args.output / "source_snapshot.json").write_bytes(args.input.read_bytes())
    proposals = [{"id": r["id"], "field": "reference", "before": original[r["id"]]["reference"],
                  "after": r["proposed_reference"], "reason": r["finding"], "source_ids": r["source_ids"],
                  "target_claim_status": "unverifiable", "data_role": "uncertainty_probe", "approved_for_final_test": False}
                 for r in payload["reviews"] if r["disposition"] == "reference_issue"]
    (args.output / "reference_proposals.json").write_text(json.dumps(proposals, ensure_ascii=False, indent=2), encoding="utf-8")
    with (args.output / "actions.csv").open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=["id", "question", "disposition", "finding", "next_step", "source_ids"])
        writer.writeheader()
        writer.writerows({**{k: r[k] for k in ("id", "disposition", "finding", "next_step")},
                          "question": original[r["id"]]["question"], "source_ids": ";".join(r["source_ids"])} for r in payload["reviews"])
    lines = ["# 17条待核验实体题补查", "", "这是AI开发者补查，独立人工复核仍为0。首轮台账与实验输入保持原样，本报告作为附加证据，不把原有17条自动改为已核实。", "",
             f"逐题覆盖17项：{counts.get('reference_issue', 0)}项发现参考表述问题，{counts.get('context_only', 0)}项取得有限背景，{counts.get('pending_source_review', 0)}项仍无可用的具体原始来源。三类均未建立题设身份或产品主张的完整真值。", "",
             "## 实质性发现", "", "同名科研人员的官网记录反驳了原参考对姓名的笼统不存在断言，不能把这些真人的身份和工作自动等同于题设身份。小米已展示YU7，原参考仅有SU7及衍生款的背景过时；YU7不是SU9的参数证据。四条具体候选修改见reference_proposals.json，全部未批准用于正式测试。", "",
             "## 逐题处理", "", "| ID | 补查结果 | 结论边界与下一步 |", "| --- | --- | --- |"]
    for review in payload["reviews"]:
        lines.append(f"| {review['id']} | {review['disposition']} | {review['finding']} {review['next_step']} |")
    lines.extend(["", "## 来源与访问边界", ""])
    for source in payload["sources"]:
        lines.extend([f"### {source['id']}", "", f"[{source['title']}]({source['url']})；访问方式：{source['access_method']}。定位：{source['locator']}。", "",
                      source["supports"], source["does_not_support"], ""])
    lines.extend(["## 访问失败与使用限制", "", "ACM完整名录原站403，部分联合国原站403，安庆师范大学人员页原站超时。实际读取搜索索引正文的来源明确标为indexed_body，未把访问失败记为原站已核实。搜索无相关命中也不作为不存在证明。", "",
                  "参考修订、来源核验、题设真值和人工批准分别保存。22条不确定性探针的数据用途不变；新证据不自动进入RAG、历史模型提示或评分结果。需要有事实真值的后续任务，应先提供可核对的封闭材料，并作为新开发诊断单列。", ""])
    (args.output / "report.md").write_text("\n".join(lines), encoding="utf-8")
    manifest = {"stage": "developer_followup_not_frozen_test", "counts": counts, "items": len(payload["reviews"]),
                "sources": len(payload["sources"]), "reference_proposals": len(proposals), "independent_human_reviews": 0,
                "followup_sha256": sha256_file(args.input), "unchanged_frozen_inputs": frozen}
    if any(sha256_file(ROOT / p) != expected for p, expected in frozen.items()):
        raise ValueError("Frozen inputs changed during follow-up generation")
    (args.output / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in manifest.items() if k != "unchanged_frozen_inputs"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
