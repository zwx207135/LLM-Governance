"""Read-only screening of historical outputs; never changes answers or manual judgments."""
import json
from collections import Counter
from pathlib import Path
from src.governance.consistency import check_consistency
from src.utils.experiment_io import latest_records, read_records, sha256_file

ROOT = Path(__file__).resolve().parents[1]
RUNS = ("expanded_v3", "controls_v3", "policy_comparison_v1", "demo_v1", "source_bound_v1", "structured_v1", "balanced_materials_v1", "balanced_labels_cn_v1")


def main():
    output = ROOT / "docs/c_work/consistency_audit_v1"
    output.mkdir(exist_ok=False)
    rows, inputs = [], {}
    for name in RUNS:
        run = ROOT / "docs/c_work/runs" / name
        path = run / "records.jsonl"
        inputs[name] = sha256_file(path)
        controls = run / "controls.json"
        items = json.loads(controls.read_text(encoding="utf-8"))["items"] if controls.exists() else []
        materials = {str(i["id"]): i.get("materials", []) for i in items}
        for r in latest_records(read_records(path)).values():
            if r["status"] != "ok":
                continue
            labels = r.get("evidence_labels")
            if not labels and r.get("policy") in ("compact", "guarded"):
                labels = {str(i): h["id"] for i, h in enumerate(r.get("evidence", []), 1)}
            result = check_consistency(r["answer"], r.get("evidence", []), labels, materials.get(str(r["id"]), []))
            rows.append({"run": name, "id": r["id"], "mode": r["mode"], **result})
        if sha256_file(path) != inputs[name]:
            raise ValueError("Historical answer log changed")
    counts = Counter(f["code"] for r in rows for f in r["flags"])
    summary = {"records_checked": len(rows), "flagged_records": sum(bool(r["flags"]) for r in rows),
               "signals": dict(counts), "input_sha256": inputs, "factual_accuracy": None,
               "scope": "Signals only; unflagged does not mean supported. No semantic entailment assessed."}
    (output / "checks.json").write_text(json.dumps({"summary": summary, "records": rows}, ensure_ascii=False, indent=2), encoding="utf-8")
    (output / "report.md").write_text("# 历史输出一致性筛查\n\n" + json.dumps(summary, ensure_ascii=False, indent=2) + "\n\n机械检查包括未知编号、映射错误和结论/依据字段冲突。URL或数值信号只是待审线索；不能判断被引用资料是否真正支持整段陈述，未触发也不表示事实正确。原回答及人工评分未改写。\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
