"""C1 proposals only: preserve original questions and keep bounded alternatives separate."""
import argparse
import json
import sys
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.utils.experiment_io import sha256_file

FROZEN = ("datasets/hallucination/test_set.json", "docs/c_work/source_followup_v1.json", "docs/c_work/data_audit.json",
          "docs/c_work/source_registry.json", "docs/c_work/development_dataset.json", "knowledge/corpus_v3.json", "knowledge/corpus_v4.json")


def validate(payload, original, previous):
    expected = {r["id"] for r in previous["reviews"] if r["disposition"] == "pending_source_review"}
    rows = payload["reviews"]
    if len(rows) != len(expected) or {r["id"] for r in rows} != expected:
        raise ValueError("Cover exactly the previous still-pending cases")
    if payload.get("reviewer_type") != "ai_developer" or payload.get("independent_human_reviews_completed") != 0:
        raise ValueError("Developer follow-up cannot impersonate independent human review")
    sources = {s["id"]: s for s in payload["sources"]}
    if len(sources) != len(payload["sources"]):
        raise ValueError("Duplicate source identity")
    checked = date.fromisoformat(payload["checked_at"])
    for source in sources.values():
        parsed = urlparse(source["url"])
        if parsed.scheme != "https" or not parsed.netloc or source["access_method"] not in ("direct_body", "indexed_body"):
            raise ValueError("HTTPS and actual access method required")
        if date.fromisoformat(source["accessed_at"]) > checked:
            raise ValueError("Access date cannot follow the declared check date")
        if not all(source.get(k) for k in ("locator", "observed_facts", "supports", "does_not_support")):
            raise ValueError("Every source needs a locator, observed facts and limits")
    originals = {r["id"]: r for r in original["items"]}
    candidate_ids = []
    for row in rows:
        if row["id"] not in originals or not row.get("queries") or not row.get("source_ids"):
            raise ValueError("Bind each proposal to original identity and actual source attempts")
        if any(s not in sources for s in row["source_ids"]):
            raise ValueError("Unregistered source")
        if row.get("target_claim_status") not in ("unresolved_identity", "unresolved_service_and_date", "unresolved_feature_and_version"):
            raise ValueError("Contextual evidence cannot silently verify the original target claim")
        if row.get("approved_for_final_test", False) or row.get("approved", False):
            raise ValueError("No automatic approval of developer proposals")
        if not all(row.get(k) for k in ("finding", "proposed_reference", "required_identifiers", "candidate_id", "candidate_question", "candidate_material", "candidate_expected_scope")):
            raise ValueError("A concrete original-reference proposal and bounded alternative are required")
        if row["candidate_question"] == originals[row["id"]]["question"]:
            raise ValueError("Alternative task must be identified as a changed question")
        candidate_ids.append(row["candidate_id"])
    if len(candidate_ids) != len(set(candidate_ids)):
        raise ValueError("Duplicate alternative question identity")
    return originals


def verify(folder):
    manifest = json.loads((folder / "manifest.json").read_text(encoding="utf-8"))
    for name, expected in manifest["artifact_sha256"].items():
        if sha256_file(folder / name) != expected:
            raise ValueError("Changed C1 artifact: " + name)
    for name, expected in manifest["unchanged_frozen_inputs"].items():
        if sha256_file(ROOT / name) != expected:
            raise ValueError("Original data/knowledge changed after C1 follow-up: " + name)
    payload = json.loads((folder / "source_snapshot.json").read_text(encoding="utf-8"))
    original = json.loads((ROOT / "datasets/hallucination/test_set.json").read_text(encoding="utf-8"))
    prior = json.loads((ROOT / "docs/c_work/source_followup_v1.json").read_text(encoding="utf-8"))
    originals = validate(payload, original, prior)
    references = json.loads((folder / "reference_proposals.json").read_text(encoding="utf-8"))
    candidates = json.loads((folder / "bounded_candidates.json").read_text(encoding="utf-8"))["items"]
    if len(references) != len(payload["reviews"]) or len(candidates) != len(references):
        raise ValueError("Proposal counts differ")
    for row, proposal, candidate in zip(payload["reviews"], references, candidates):
        if proposal["id"] != row["id"] or proposal["question"] != originals[row["id"]]["question"] or proposal["before"] != originals[row["id"]]["reference"]:
            raise ValueError("Proposal altered the original question or before value")
        if proposal["after"] != row["proposed_reference"] or candidate["source_original_id"] != row["id"] or candidate["id"] != row["candidate_id"]:
            raise ValueError("Proposal differs from source snapshot")
        if proposal["approved_for_final_test"] or candidate["approved_for_final_test"] or not candidate["question_is_changed"]:
            raise ValueError("Question transformation or approval status hidden")
    return {"original_cases_still_unresolved": len(references), "reference_proposals": len(references),
            "bounded_alternative_candidates": len(candidates), "sources": len(payload["sources"]),
            "original_questions_and_knowledge_unchanged": True, "model_calls": 0, "independent_human_reviews": 0}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=ROOT / "docs/c_work/source_followup_pending_v2.json")
    parser.add_argument("--output", type=Path, default=ROOT / "docs/c_work/pending_repairs_v2")
    parser.add_argument("--verify", type=Path)
    args = parser.parse_args()
    if args.verify:
        print(json.dumps(verify(args.verify), ensure_ascii=False, indent=2))
        return
    payload = json.loads(args.input.read_text(encoding="utf-8"))
    data = json.loads((ROOT / FROZEN[0]).read_text(encoding="utf-8"))
    prior = json.loads((ROOT / FROZEN[1]).read_text(encoding="utf-8"))
    originals = validate(payload, data, prior)
    frozen = {name: sha256_file(ROOT / name) for name in FROZEN}
    args.output.mkdir(parents=True, exist_ok=False)
    (args.output / "source_snapshot.json").write_bytes(args.input.read_bytes())
    proposals, candidates = [], []
    for row in payload["reviews"]:
        proposals.append({"id": row["id"], "question": originals[row["id"]]["question"], "field": "reference",
                          "before": originals[row["id"]]["reference"], "after": row["proposed_reference"], "reason": row["finding"],
                          "source_ids": row["source_ids"], "target_claim_status": row["target_claim_status"],
                          "data_role": "uncertainty_probe", "approved_for_final_test": False})
        candidates.append({"id": row["candidate_id"], "source_original_id": row["id"], "question": row["candidate_question"],
                           "materials": [{"source_id": row["source_ids"][0], "text": row["candidate_material"], "kind": "developer_paraphrase"}],
                           "expected_scope": row["candidate_expected_scope"], "source_ids": row["source_ids"],
                           "question_is_changed": True, "data_role": "bounded_revision_candidate_not_frozen_test",
                           "approved_for_final_test": False})
    for name, obj in [("reference_proposals.json", proposals), ("bounded_candidates.json", {"stage": "C1_reviewable_candidates_only", "items": candidates})]:
        (args.output / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = ["# C1：五条待核验题的补查与修订候选", "", "2026-11-24。本轮仅完成C的数据核验意见：5条原题参考表述提案、5条限定材料的新题候选、5个来源。没有新增模型调用或正式评分。五个原始目标仍未建立完整身份/产品真值，不把处理完提案称为五题已核实。", "",
             "## 原题与候选分开", "", "原题继续作为不确定性探针；参考提案去除超出证据的不存在断言。新候选明确改变题目、带材料和支持范围，不覆盖原题，也不自动进入RAG或正式题集。预期范围只是C的开发核验意见，不是独立人工批准。", "",
             "| 原题 | 具体发现 | 仍缺什么 | 新候选 |", "| --- | --- | --- | --- |"]
    for row in payload["reviews"]:
        lines.append(f"| {row['id']} | {row['finding']} | {'、'.join(row['required_identifiers'])} | {row['candidate_id']} |")
    lines.extend(["", "## 可逐条审核的改动", ""])
    for row, proposal, candidate in zip(payload["reviews"], proposals, candidates):
        lines.extend([f"### 原题{row['id']} / {candidate['id']}", "", "原问题：" + proposal["question"], "", "原参考：" + proposal["before"], "",
                      "参考表述提案：" + proposal["after"], "", "新题候选（问题已改变）：" + candidate["question"], "",
                      "给定材料（开发者转述）：" + candidate["materials"][0]["text"], "", "预期支持范围（待复核）：" + candidate["expected_scope"], ""])
    lines.extend(["## 来源与访问边界", ""])
    for source in payload["sources"]:
        lines.extend([f"- [{source['title']}]({source['url']})；{source['access_method']}；定位：{source['locator']}。支持：{source['supports']} 限制：{source['does_not_support']}", ""])
    lines.extend(["## 不应混淆的状态", "", "搜索无命中、访问失败、企业年报列出常规业务、同一集团报告包含两个关键词，都不自动支持目标不存在或功能已经上线。作品标题、简介措辞、译名、城市、运营主体和报告期间须分别核对。", "",
                  "原第33题参考中的本题虚构声明需要合成题构造记录和封闭任务说明，不能代替开放世界书目不存在的证据。第34题的单届奥斯卡名单不能穷尽全部历史。第37题奥克兰塔高不能回答上海项目。第41/42题旧年度报告不涵盖全部后续版本。", "",
                  "未采用的聚合页、近名内容和二手业务消息见source_snapshot.json的excluded_leads。只读取目录而非业务正文的页面，未记成正文已核实。", "",
                  "参考表述、原题目标真值、新题预期范围、最终批准四种状态分开保存。原初审、v1补查、原题、v3/v4语料和旧模型回答均保留。"])
    (args.output / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (args.output / "builder_snapshot.py").write_bytes(Path(__file__).read_bytes())
    artifacts = [p.name for p in args.output.iterdir() if p.is_file()]
    manifest = {"stage": "C1_proposals_only_not_approved", "input_sha256": sha256_file(args.input),
                "artifact_sha256": {name: sha256_file(args.output / name) for name in artifacts}, "unchanged_frozen_inputs": frozen,
                "model_calls": 0, "independent_human_reviews": 0}
    (args.output / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(verify(args.output), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
