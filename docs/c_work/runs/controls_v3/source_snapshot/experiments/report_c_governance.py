"""Export measured run statistics and an unscored independent-review worksheet."""
import argparse
import csv
import json
from collections import Counter
from pathlib import Path
from statistics import mean


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run", type=Path)
    args = parser.parse_args()
    manifest = json.loads((args.run / "manifest.json").read_text(encoding="utf-8"))
    if manifest["status"] != "completed" or manifest["dry_run"]:
        raise ValueError("A completed real model run is required")
    rows = [json.loads(line) for line in (args.run / "records.jsonl").read_text(encoding="utf-8").splitlines()]
    expected = {(i, m) for i in manifest["config"]["development_ids"] for m in manifest["modes"]}
    actual = [(r["id"], r["mode"]) for r in rows]
    if len(actual) != len(set(actual)) or set(actual) != expected or any(r["status"] != "ok" for r in rows):
        raise ValueError("Run has missing, duplicate, or failed records")
    table = []
    for mode in manifest["modes"]:
        group = [r for r in rows if r["mode"] == mode]
        table.append({"mode": mode, "n": len(group), "mean_generation_seconds": round(mean(r["generation_seconds"] for r in group), 4),
                      "mean_output_tokens": round(mean(r["output_tokens"] for r in group), 1),
                      "truncated": sum(r["truncated"] for r in group),
                      "retrieval_status": dict(Counter(r["retrieval_status"] for r in group))})
    summary = {"stage": "development_only", "n_questions": len(manifest["config"]["development_ids"]),
               "n_answers": len(rows), "modes": table, "accuracy": None, "hallucination_rate": None,
               "evaluation_status": "pending_independent_review"}
    (args.run / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    fields = ["id", "mode", "question", "answer", "truncated", "evidence_ids", "source_urls", "core_correct", "contains_false_fact", "accepts_false_premise", "unsupported_citation", "refusal", "evidence_relevant", "evidence_supports_answer", "reviewer", "rationale", "second_reviewer"]
    with (args.run / "review.csv").open("w", newline="", encoding="utf-8-sig") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        for r in rows:
            writer.writerow({"id": r["id"], "mode": r["mode"], "question": r["question"], "answer": r["answer"],
                             "truncated": r["truncated"], "evidence_ids": ";".join(h["id"] for h in r["evidence"]),
                             "source_urls": ";".join(h["source"]["url"] for h in r["evidence"])})
    lines = ["# C 开发实验记录", "", f"{summary['n_questions']}道开发题的配置对照用于验证流程与发现问题。尚未独立评分，不据此报告正确率或幻觉下降幅度。", "",
             "| 配置 | 回答数 | 平均生成秒数 | 平均输出token | 截断数 |", "| --- | ---: | ---: | ---: | ---: |"]
    for r in table:
        lines.append(f"| {r['mode']} | {r['n']} | {r['mean_generation_seconds']} | {r['mean_output_tokens']} | {r['truncated']} |")
    lines.extend(["", "计时包含分词、推理和解码，GPU已同步；模型加载、首次预热及检索准备不计入生成耗时。检索准备耗时逐条另存。", "",
                  "四种模式分别为原始模型、仅回答约束、仅检索资料、检索加回答约束。后两组数学题跳过检索。", ""])
    for ident in manifest["config"]["development_ids"]:
        group = [r for r in rows if r["id"] == ident]
        lines.extend([f"## 第{ident}题", "", group[0]["question"], ""])
        for r in group:
            lines.extend([f"### {r['mode']}", "", f"检索状态：{r['retrieval_status']}；生成耗时：{r['generation_seconds']}秒；截断：{r['truncated']}。", "", r["answer"], ""])
            for hit in r["evidence"]:
                lines.extend([f"资料 {hit['id']}：{hit['text']}", "", f"来源：[{hit['source']['title']}]({hit['source']['url']})", ""])
    (args.run / "report.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
