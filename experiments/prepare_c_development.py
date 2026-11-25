"""Create a development-only usage ledger; uncertain entities never become false gold labels."""
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

LEAKAGE_GROUPS = [
    [5, 88], [6, 86], [16, 80, 91], [19, 81, 99], [21, 87, 92],
    [25, 94], [28, 76, 77, 79, 89, 95], [107, 117],
]


def prepare(audit, candidates):
    original = {x["id"]: x for x in audit["items"]}
    candidate = {x["id"]: x for x in candidates["items"]}
    if set(original) != set(candidate):
        raise ValueError("Candidate and audit IDs differ")
    selected = set([1, 3, 4, 5, 6, 7, 9, 10, 11, 14, 16, 17, 18, 19, 25]
                   + list(range(26, 51))
                   + [51, 52, 53, 54, 55, 56, 59, 60, 61, 62, 63, 64, 65, 66, 73]
                   + [76, 77, 79, 80, 81, 83, 84, 85, 86, 88, 89, 91, 93, 94, 99]
                   + list(range(101, 116)))
    # All known equivalent/strongly related forms stay together. No formal test is declared.
    for group in LEAKAGE_GROUPS:
        if selected.intersection(group):
            selected.update(group)
    records, usage = [], []
    for ident in sorted(original):
        row = original[ident]
        uncertainty = row["category"] == "fictional_entity" and ident not in (27, 30, 31)
        if row["source_verification_status"] in ("pending_source_review", "limited_scope"):
            uncertainty = True
        purpose = "uncertainty_probe" if uncertainty else "provisional_reference"
        record = dict(candidate[ident])
        record["data_role"] = purpose
        if uncertainty:
            # Retain disputed references only in the audit ledger, not as truth labels in a run.
            record["reference"] = None
            record["reference_source"] = None
            record["note"] = "身份/实体/产品未充分核实。观察不确定性处理，不凭原参考断言不存在。"
        record["approved_for_final_test"] = False
        records.append(record)
        usage.append({"id": ident, "category": row["category"], "data_role": purpose,
                      "run_in_expanded_development": ident in selected,
                      "reason": "参考不足，不计算事实正确率" if uncertainty else "候选参考有来源或修订依据，仍待独立复核",
                      "formal_test_status": "not_designated", "approved_for_final_test": False})
    return records, usage, sorted(selected)


def main():
    output = ROOT / "docs/c_work"
    audit_path = output / "data_audit.json"
    candidate_path = output / "reviewed_candidate.json"
    records, usage, selected = prepare(json.loads(audit_path.read_text(encoding="utf-8")),
                                      json.loads(candidate_path.read_text(encoding="utf-8")))
    def write(path, value):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")
    write(output / "development_dataset.json", {"stage": "development_only_not_frozen_test", "items": records})
    summary = {"items": len(usage), "roles": dict(Counter(r["data_role"] for r in usage)),
               "development_questions": len(selected), "unused_in_this_run": len(usage) - len(selected),
               "development_categories": dict(Counter(r["category"] for r in usage if r["run_in_expanded_development"])),
               "audit_sha256": hashlib.sha256(audit_path.read_bytes()).hexdigest(),
               "candidate_sha256": hashlib.sha256(candidate_path.read_bytes()).hexdigest()}
    write(output / "data_usage.json", {"summary": summary, "known_groups": LEAKAGE_GROUPS, "items": usage})
    config = {"version": "c-dev-expanded-v3", "dataset": "docs/c_work/development_dataset.json",
              "corpus": "knowledge/corpus_v3.json", "model_path": "models/Qwen2.5-0.5B-Instruct",
              "generation": {"max_new_tokens": 192, "do_sample": False}, "seed": 20261122,
              "retrieval": {"top_k": 2, "min_score": 1.5},
              "modes": ["baseline", "constraint", "retrieval", "combined"], "development_ids": selected}
    write(ROOT / "configs/c_expanded.json", config)
    controls = json.loads((ROOT / "datasets/controls/c_normal_development.json").read_text(encoding="utf-8"))
    write(ROOT / "configs/c_controls.json", {**config, "version": "c-normal-controls-v1",
          "dataset": "datasets/controls/c_normal_development.json", "development_ids": [x["id"] for x in controls["items"]]})
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
