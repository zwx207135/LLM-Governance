"""Strict conformance checks for six closed-format controls, not general answer quality."""
import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.utils.experiment_io import latest_records, read_records

CHECKED_IDS = {"N07", "N08", "N09", "N10", "N11", "N15"}


def check(ident, answer):
    text = answer.strip()
    if ident == "N07":
        return re.sub(r"[\s、，,。.]", "", text) == "笔记本充电器学生证"
    if ident == "N08":
        return re.sub(r"[\s。.]", "", text) == "核查来源"
    if ident == "N09":
        return re.sub(r"\s", "", text) == "2026年11月22日"
    if ident == "N10":
        return bool(re.fullmatch(r"[\d\s、，,]+", text)) and re.findall(r"\d+", text) == ["3", "5", "8", "11"]
    if ident == "N11":
        return re.sub(r"[\s，]", lambda m: "," if m.group() == "，" else "", text) == "APPLE,BOOK,CAT"
    if ident == "N15":
        try:
            return json.loads(text) == {"name": "小林", "task": "检索"}
        except (ValueError, TypeError):
            return False
    raise ValueError("No strict rule for this open-ended task")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run", type=Path)
    args = parser.parse_args()
    manifest = json.loads((args.run / "manifest.json").read_text(encoding="utf-8"))
    if manifest["status"] != "completed" or manifest["contract"]["dry_run"]:
        raise ValueError("A completed real run is required")
    modes = manifest["contract"]["config"]["modes"]
    rows = list(latest_records(read_records(args.run / "records.jsonl")).values())
    relevant = [r for r in rows if str(r["id"]) in CHECKED_IDS]
    expected = {(ident, mode) for ident in CHECKED_IDS for mode in modes}
    if {(str(r["id"]), r["mode"]) for r in relevant} != expected:
        raise ValueError("Missing strict-format controls")
    checks = [{"id": r["id"], "mode": r["mode"], "answer": r["answer"],
               "passed": check(str(r["id"]), r["answer"]), "label_type": "closed_format_conformance_only"} for r in relevant]
    summary = {"scope": "六道明确指定输出格式的开发题；不评价其余十四道开放任务，不代表正确率或幻觉率。",
               "modes": [{"mode": m, "passed": sum(r["passed"] for r in checks if r["mode"] == m),
                          "checked": len(CHECKED_IDS)} for m in modes]}
    (args.run / "format_checks.json").write_text(json.dumps({"summary": summary, "items": checks}, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = ["# 正常任务输出格式检查", "", summary["scope"], "", "| 配置 | 符合格式 |", "| --- | ---: |"]
    for row in summary["modes"]:
        lines.append(f"| {row['mode']} | {row['passed']}/{row['checked']} |")
    lines.extend(["", "检查任务为物品列表、只输出任务名、中文日期、数值排序、大写英文词与合法JSON。额外解释、错误顺序或不符合指定格式均不通过此项，不能据此断言整个回答无用或含幻觉。", ""])
    (args.run / "format_checks.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
