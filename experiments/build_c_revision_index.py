"""C1 revision index: preserve alternatives, provenance and approval boundaries."""
import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.utils.experiment_io import sha256_file, stable_hash

INPUTS = ("datasets/hallucination/test_set.json", "docs/c_work/data_audit.json", "docs/c_work/data_change_proposals.json",
          "docs/c_work/source_followup_v1/reference_proposals.json", "docs/c_work/source_followup_v1.json",
          "docs/c_work/pending_repairs_v2/reference_proposals.json", "docs/c_work/source_followup_pending_v2.json",
          "docs/c_work/pending_repairs_v2/bounded_candidates.json")


def assemble(original, audit, batches, source_payloads, candidates):
    originals = {r["id"]: r for r in original["items"]}
    audits = {r["id"]: r for r in audit["items"]}
    sources, reviews = {}, {}
    for payload in source_payloads:
        for source in payload["sources"]:
            if source["id"] in sources and sources[source["id"]] != source:
                raise ValueError("Source identity collision")
            sources[source["id"]] = source
        reviews.update({r["id"]: r for r in payload["reviews"]})
    items, groups = [], defaultdict(list)
    for batch_name, proposals in batches:
        for index, proposal in enumerate(proposals):
            ident, field = proposal["id"], proposal["field"]
            if ident not in originals or field not in ("question", "reference"):
                raise ValueError("Unknown original item or field")
            if originals[ident][field] != proposal["before"]:
                raise ValueError("Before value differs from frozen original")
            if proposal.get("approved_for_final_test", False):
                raise ValueError("Index cannot silently adopt approved replacements")
            linked_sources = []
            for sid in proposal.get("source_ids", []):
                if sid not in sources:
                    raise ValueError("Unregistered source " + sid)
                linked_sources.append(sources[sid])
            if not linked_sources:
                linked_sources = audits[ident].get("resolved_sources", [])
            review = reviews.get(ident, {})
            item = {"proposal_id": f"{batch_name}:{index + 1}", "original_id": ident, "field": field,
                    "original_question": originals[ident]["question"], "before": proposal["before"], "after": proposal["after"],
                    "reason": proposal["reason"], "batch": batch_name, "source_row_sha256": stable_hash(proposal),
                    "sources": linked_sources, "source_review_status": audits[ident]["source_verification_status"],
                    "target_claim_status": proposal.get("target_claim_status", "see_source_review_not_final_truth"),
                    "evidence_scope": [{"source_id": s.get("id"), "url": s["url"],
                                        "supports": s.get("supports", s.get("locator")), "limits": s.get("does_not_support", "仅按原核验定位解释；不外推附加事实。")}
                                       for s in linked_sources],
                    "missing_identifiers": review.get("required_identifiers", []),
                    "followup_action": review.get("next_step"), "changes_question": field == "question",
                    "approved_for_final_test": False, "auto_applied": False}
            items.append(item)
            groups[ident, field].append(item)
    conflicts = [{"original_id": ident, "field": field, "proposal_ids": [r["proposal_id"] for r in rows],
                  "different_candidate_values": len({r["after"] for r in rows}),
                  "status": "manual_resolution_required" if len({r["after"] for r in rows}) > 1 else "identical_values_multiple_provenance"}
                 for (ident, field), rows in sorted(groups.items()) if len(rows) > 1]
    alternatives = []
    for candidate in candidates["items"]:
        if candidate["source_original_id"] not in originals or candidate["approved_for_final_test"] or not candidate["question_is_changed"]:
            raise ValueError("Bounded alternative misrepresented as original approved item")
        alternatives.append({**candidate, "not_an_original_field_patch": True})
    return {"stage": "C1_developer_revision_index_not_approved", "proposals": items, "overlapping_field_groups": conflicts,
            "bounded_alternatives": alternatives, "selected_replacement": None,
            "synthetic_origin_note": {"original_id": 33, "declared_in_original_reference": "本题虚构",
                                      "construction_record_available": False,
                                      "boundary": "原参考的合成声明不证明开放世界中同名作品不存在；须保存构造记录并声明封闭任务。"},
            "summary": {"proposal_entries": len(items), "distinct_original_items": len({r["original_id"] for r in items}),
                        "field_counts": dict(Counter(r["field"] for r in items)), "overlap_groups": len(conflicts),
                        "conflicting_groups": sum(r["different_candidate_values"] > 1 for r in conflicts),
                        "bounded_alternatives": len(alternatives), "approved_replacements": 0, "independent_human_reviews": 0}}


def load_payload():
    values = [json.loads((ROOT / name).read_text(encoding="utf-8")) for name in INPUTS]
    return assemble(values[0], values[1], [("initial", values[2]), ("followup_v1", values[3]), ("pending_v2", values[5])],
                    [values[4], values[6]], values[7])


def verify(folder):
    manifest = json.loads((folder / "manifest.json").read_text(encoding="utf-8"))
    for name, expected in manifest["inputs_sha256"].items():
        if sha256_file(ROOT / name) != expected:
            raise ValueError("Index input changed: " + name)
    for name, expected in manifest["artifacts_sha256"].items():
        if sha256_file(folder / name) != expected:
            raise ValueError("Index artifact changed: " + name)
    actual = json.loads((folder / "index.json").read_text(encoding="utf-8"))
    if actual != load_payload():
        raise ValueError("Index does not reproduce from original proposals")
    return actual["summary"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "docs/c_work/revision_index_v1")
    parser.add_argument("--verify", type=Path)
    args = parser.parse_args()
    if args.verify:
        print(json.dumps(verify(args.verify), ensure_ascii=False))
        return
    payload = load_payload()
    args.output.mkdir(parents=True, exist_ok=False)
    (args.output / "index.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    summary = payload["summary"]
    lines = ["# C1统一修订索引", "", "汇总原始逐字段提案、17题补查提案和剩余五题提案。索引不批准或自动应用修改，原题和各批提案保留。", "",
             f"共{summary['proposal_entries']}条字段提案，涉及{summary['distinct_original_items']}道原题：{summary['field_counts']}。原19题实际包含21条字段改动，不能把题数与字段条数混用。另有5道限定材料新题候选，明确单列而非原题补丁。", "",
             f"同一原题同一字段重叠组：{summary['overlap_groups']}；不同候选值冲突组：{summary['conflicting_groups']}。没有冲突不表示事实已批准。", "",
             "| 原题 | 字段 | 批次 | 来源数 | 改变问题 | 批准 |", "| --- | --- | --- | ---: | --- | --- |"]
    for row in payload["proposals"]:
        lines.append(f"| {row['original_id']} | {row['field']} | {row['batch']} | {len(row['sources'])} | {'是' if row['changes_question'] else '否'} | 未批准 |")
    lines.extend(["", "详细原值、候选值、理由、来源与范围、缺失标识、来源记录哈希见[index.json](index.json)。尚未补足的标识不可从同名或近名实体推断。", "",
                  "第33题的合成虚构声明单独登记；构造记录未提供，不能解释为开放世界书目不存在。材料新题的预期范围也是开发意见，不是独立人工真值。", "",
                  "全部替换均auto_applied=false、approved_for_final_test=false。该索引不进入知识库、模型提示或正式题集。"])
    (args.output / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (args.output / "builder_snapshot.py").write_bytes(Path(__file__).read_bytes())
    manifest = {"inputs_sha256": {name: sha256_file(ROOT / name) for name in INPUTS},
                "artifacts_sha256": {p.name: sha256_file(p) for p in args.output.iterdir() if p.is_file()}}
    (args.output / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(verify(args.output), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
