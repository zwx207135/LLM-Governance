"""Measure topic retrieval on 30 developer-authored probes, not factual answer quality."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.governance.retrieval import LocalRetriever


def main():
    checks = json.loads((ROOT / "knowledge/retrieval_checks.json").read_text(encoding="utf-8"))
    retriever = LocalRetriever(ROOT / "knowledge/corpus_v3.json")
    rows = []
    for case in checks["cases"]:
        hits = retriever.search(case["question"], top_k=2)
        expected = set(case["expected_chunks"])
        rank = next((i for i, h in enumerate(hits, 1) if h["id"] in expected), None)
        rows.append({**case, "retrieved": hits, "relevant_hit_at_2": rank is not None if expected else None,
                     "reciprocal_rank": 1 / rank if rank else 0,
                     "no_hit_correct": not hits if not expected else None,
                     "support_review_type": "developer_authored_source_scope_not_independent_annotation"})
    positives = [r for r in rows if r["expected_chunks"]]
    negatives = [r for r in rows if not r["expected_chunks"]]
    summary = {"stage": checks["stage"], "cases": len(rows), "answerable_source_probes": len(positives),
               "hit_at_2_numerator": sum(r["relevant_hit_at_2"] for r in positives),
               "hit_at_2_denominator": len(positives),
               "mean_reciprocal_rank_at_2": sum(r["reciprocal_rank"] for r in positives) / len(positives),
               "negative_no_hit_numerator": sum(r["no_hit_correct"] for r in negatives),
               "negative_no_hit_denominator": len(negatives), "corpus_sha256": retriever.sha256,
               "interpretation": "仅衡量开发者所列相关资料是否召回；不代表模型正确率、引用支持率或独立检索基准成绩。"}
    output = ROOT / "docs/c_work"
    (output / "retrieval_diagnostics.json").write_text(json.dumps({"summary": summary, "items": rows}, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = ["# 检索开发诊断", "", summary["interpretation"], "",
             f"30条诊断中，相关资料在前两位命中{summary['hit_at_2_numerator']}/{len(positives)}；无资料探针正确未命中{summary['negative_no_hit_numerator']}/{len(negatives)}。", "",
             "每条支持范围由开发者依据资料片段编写，尚未经过第二人独立标注。", "",
             "| ID | 查询 | 期望资料 | 实际前两位 |", "| --- | --- | --- | --- |"]
    for row in rows:
        lines.append(f"| {row['id']} | {row['question']} | {', '.join(row['expected_chunks']) or '无资料'} | {', '.join(h['id'] for h in row['retrieved']) or '未命中'} |")
    (output / "retrieval_diagnostics.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
