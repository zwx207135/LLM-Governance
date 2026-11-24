"""Export a paired run report and preserve independent annotations across regeneration."""
import argparse
import csv
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path
from statistics import mean, median

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.utils.experiment_io import atomic_json, latest_records, read_records, stable_hash

MANUAL = ["core_correct", "contains_false_fact", "accepts_false_premise", "unsupported_citation", "refusal",
          "evidence_relevant", "evidence_supports_answer", "reviewer", "reviewer_type", "rationale", "second_reviewer"]


def content_key(row):
    return stable_hash({k: str(row.get(k, "")) for k in ("id", "mode", "question", "answer")})


def write_reviews(path, rows):
    old = {}
    if path.exists():
        raw = path.read_bytes()
        with path.open(encoding="utf-8-sig", newline="") as stream:
            previous = list(csv.DictReader(stream))
        old = {content_key(r): r for r in previous}
        if any(any(r.get(k) for k in MANUAL) for r in previous):
            archive = path.with_name(f"review.previous-{hashlib.sha256(raw).hexdigest()[:12]}.csv")
            if not archive.exists():
                archive.write_bytes(raw)
    fields = ["id", "mode", "category", "data_role", "question", "answer", "reference_for_review_only",
              "truncated", "evidence_ids", "source_urls", "screening_flags", "content_sha256"] + MANUAL
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            key = content_key(row)
            writer.writerow({**row, "content_sha256": key, **{k: old.get(key, {}).get(k, "") for k in MANUAL}})


def screen(row):
    if row["status"] != "ok":
        return ["generation_error"]
    flags = []
    answer = row.get("answer") or ""
    evidence = row.get("evidence", [])
    available = {h["id"] for h in evidence}
    cited = set(re.findall(r"\[([a-zA-Z0-9][a-zA-Z0-9_-]{0,63})\]", answer))
    if row.get("truncated"):
        flags.append("truncated")
    if cited - available:
        flags.append("citation_id_needs_review")
    if evidence and not available.intersection(cited):
        flags.append("no_explicit_evidence_id")
    if row.get("retrieval_status") == "no_hit":
        flags.append("knowledge_coverage_gap")
    if row.get("data_role") == "uncertainty_probe":
        flags.append("no_established_truth_label")
    if any(s in answer for s in ("无法确认", "无法核实", "无法提供", "不知道", "不确定", "不能回答", "信息不足", "没有足够")):
        flags.append("uncertainty_or_refusal_phrase")
        if row.get("data_role") == "normal_control":
            flags.append("possible_over_refusal")
    if re.match(r"^\s*来源[:：]", answer) and len(answer) < 180:
        flags.append("possible_source_only_answer")
    return flags


def summarize(rows, config):
    modes = config["modes"]
    by_mode = []
    baseline = {str(r["id"]): r for r in rows if r["mode"] == "baseline" and r["status"] == "ok"}
    for mode in modes:
        group = [r for r in rows if r["mode"] == mode]
        success = [r for r in group if r["status"] == "ok"]
        paired = [(r, baseline[str(r["id"])]) for r in success if str(r["id"]) in baseline]
        by_mode.append({"mode": mode, "planned": len(config["development_ids"]), "successful": len(success),
                        "failed": sum(r["status"] == "error" for r in group),
                        "mean_generation_seconds": round(mean(r["generation_seconds"] for r in success), 4) if success else None,
                        "median_generation_seconds": round(median(r["generation_seconds"] for r in success), 4) if success else None,
                        "mean_prepare_seconds": round(mean(r["prepare_seconds"] for r in success), 6) if success else None,
                        "mean_output_tokens": round(mean(r["output_tokens"] for r in success), 2) if success else None,
                        "truncated_numerator": sum(r["truncated"] for r in success), "truncated_denominator": len(success),
                        "retrieval_status": dict(Counter(r["retrieval_status"] for r in success)),
                        "paired_baseline_n": len(paired),
                        "paired_mean_generation_delta_seconds": round(mean(r["generation_seconds"] - b["generation_seconds"] for r, b in paired), 4) if paired else None,
                        "screening_flags": dict(Counter(flag for r in group for flag in screen(r)))})
    return {"stage": "development_only", "questions": len(config["development_ids"]), "records": len(rows),
            "successful_records": sum(r["status"] == "ok" for r in rows),
            "data_roles": dict(Counter(r.get("data_role", "unspecified") for r in rows)), "modes": by_mode,
            "accuracy": None, "hallucination_rate": None, "evaluation_status": "pending_independent_review"}


def fenced(text):
    fence = "`" * max(3, max((len(x) for x in re.findall(r"`+", text)), default=0) + 1)
    return fence + "text\n" + text + "\n" + fence


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run", type=Path)
    args = parser.parse_args()
    run = args.run
    manifest = json.loads((run / "manifest.json").read_text(encoding="utf-8"))
    if manifest.get("schema_version") != 2 or manifest["contract"]["dry_run"]:
        raise ValueError("A real schema-v2 run is required")
    if manifest["status"] not in ("completed", "completed_with_errors"):
        raise ValueError("Finish/resume the run before creating the final report")
    config = manifest["contract"]["config"]
    latest = latest_records(read_records(run / "records.jsonl"))
    expected = set(map(tuple, manifest["planned_records"]))
    if set(latest) != expected:
        raise ValueError("Missing or unexpected records")
    rows = [latest[key] for key in map(tuple, manifest["planned_records"])]
    summary = summarize(rows, config)
    atomic_json(run / "summary.json", summary)
    dataset = json.loads((run / "dataset.json").read_text(encoding="utf-8"))
    sample = {str(i["id"]): i for i in dataset["items"]}
    review_rows, queue = [], []
    for row in rows:
        flags = screen(row)
        review_rows.append({**row, "reference_for_review_only": sample[str(row["id"])].get("reference") or "",
                            "evidence_ids": ";".join(h["id"] for h in row.get("evidence", [])),
                            "source_urls": ";".join(h["source"]["url"] for h in row.get("evidence", [])),
                            "screening_flags": ";".join(flags)})
        if flags:
            queue.append({"id": row["id"], "mode": row["mode"], "flags": flags, "status": "screening_only_not_final_labels"})
    write_reviews(run / "review.csv", review_rows)
    atomic_json(run / "review_queue.json", queue)
    cases = run / "cases"
    cases.mkdir(exist_ok=True)
    for category in sorted({r["category"] for r in rows}):
        lines = [f"# {category} 开发回答", "", "以下为模型原始输出。筛查标志仅提示复核，不是正确性或幻觉标签。", ""]
        for ident in config["development_ids"]:
            group = [r for r in rows if str(r["id"]) == str(ident) and r["category"] == category]
            if not group:
                continue
            lines.extend([f"## {ident}", "", group[0]["question"], "", f"数据用途：{group[0].get('data_role')}。", ""])
            for mode in config["modes"]:
                row = next(r for r in group if r["mode"] == mode)
                lines.extend([f"### {mode}", "", f"状态：{row['status']}；检索：{row.get('retrieval_status')}；筛查：{', '.join(screen(row)) or '无筛查标志'}。", "",
                              fenced(row.get("answer") or row.get("error", "")), ""])
                for hit in row.get("evidence", []):
                    lines.extend([f"资料 {hit['id']}：{hit['text']}", "", f"来源：[{hit['source']['title']}]({hit['source']['url']})", ""])
        (cases / f"{category}.md").write_text("\n".join(lines), encoding="utf-8")
    lines = ["# C 扩大开发实验报告", "", f"本轮{summary['questions']}道题，计划{len(expected)}条回答，成功{summary['successful_records']}条。", "",
             "四组共用同一冻结输入、模型和生成设置；按样本轮换配置顺序。基线重新生成，不能与旧采样结果混用。", "",
             "| 配置 | 成功回答 | 平均生成秒数 | 中位秒数 | 平均输出token | 截断数 |", "| --- | ---: | ---: | ---: | ---: | ---: |"]
    for row in summary["modes"]:
        lines.append(f"| {row['mode']} | {row['successful']} | {row['mean_generation_seconds']} | {row['median_generation_seconds']} | {row['mean_output_tokens']} | {row['truncated_numerator']}/{row['truncated_denominator']} |")
    lines.extend(["", "生成计时包含分词、推理和解码，GPU已同步；检索准备、模型加载和预热另外记录。不同输出长度会影响耗时，不能把更快解释为治理本身效率更高。", "",
                  "## 回答与证据", ""])
    for category in sorted({r["category"] for r in rows}):
        lines.append(f"- [{category}逐条回答](cases/{category}.md)")
    lines.extend(["", "## 评分与边界", "",
                  "review.csv保留完整回答、证据、待复核字段和人工备注。重新生成按问题与回答内容匹配，保留相同记录的人工栏；内容变化时不沿用旧判断，并保存带校验值的旧表。", "",
                  "uncertainty_probe没有已建立的事实真值，不能把原题中不存在的断言当金标准。正常任务是辅助探针，不代表通用能力。所有正确性、幻觉率及拒答合理性仍待独立复核。", "",
                  "review_queue.json中的关键词、引用格式和截断标志只用于筛查；没有触发标志也不等于回答正确，出现不确定词也不等于拒答。", "",
                  "知识库按公开主题资料整理，与现有题目存在主题重叠。本轮属于开发实验，不是独立冻结测试，也不据此宣称普遍有效。", ""])
    (run / "report.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
