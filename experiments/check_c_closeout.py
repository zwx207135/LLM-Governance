"""Read-only C closeout audit: counts, source chains, extra runs and active links."""
import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from experiments.organize_c_summary import collect
from experiments.report_c_anchor_diagnostics import load_run
from experiments.report_c_joint_batch import analyze
from src.governance.retrieval_scoped import AwardScopedRetrieverV2
from src.governance.retrieval_year_alias import AwardYearAliasRetriever
from src.utils.experiment_io import sha256_file, stable_hash

ACTIVE = ("README.md", "C_PROGRESS.md", "docs/c_work/C_HANDOFF.md", "docs/c_work/C_ONLY_STATUS.md",
          "docs/c_work/C_COMPONENT_HANDOFF.md", "docs/c_work/C_EVIDENCE_USE.md", "docs/c_work/C_SUBJECT_FOCUS.md",
          "docs/c_work/C_NOBEL_SUPPLEMENT.md", "docs/c_work/C_FAILURE_EVIDENCE.md", "docs/c_work/C_CLOSEOUT.md")


def check():
    folder = ROOT / "docs/c_work"
    inventory = collect()
    if inventory != json.loads((folder / "c_work_inventory.json").read_text(encoding="utf-8")):
        raise ValueError("Saved C inventory differs from raw records")
    original = ROOT / "datasets/hallucination/test_set.json"
    if sha256_file(original) != "3477889ae807858e0763bce4c80534f7fc834e001a7136c7a47b0bd4f34892ed":
        raise ValueError("Original dataset changed")
    anchors = {name: len(load_run(name)[2]) for name in ("anchor_diagnostics_v1", "evidence_first_v1")}
    _, normal_rows = analyze(folder / "runs/normal_route_v1")
    support = json.loads((folder / "retrieval_support_30_v1.json").read_text(encoding="utf-8"))
    for key in ("inputs_sha256", "runtime_sha256"):
        for name, expected in support[key].items():
            if sha256_file(ROOT / name) != expected:
                raise ValueError("Support diagnostic input/runtime changed: " + name)
    before = AwardScopedRetrieverV2(ROOT / "knowledge/corpus_v4.json")
    after = AwardYearAliasRetriever(ROOT / "knowledge/corpus_v4.json")
    if len(support["cases"]) != 30 or dict(Counter(r["support_judgment"] for r in support["cases"])) != support["counts"]:
        raise ValueError("Thirty-case support count differs")
    for row in support["cases"]:
        if row["inspection_origin"] != "AI_developer_not_independent_human":
            raise ValueError("Developer support inspection mislabeled")
        if before.search(row["question"]) != row["v2_evidence"] or after.search_with_diagnostics(row["question"]) != row["year_alias_diagnostics"]:
            raise ValueError("Retrieval support evidence replay differs")
    ledger = json.loads((folder / "failure_evidence_ledger_v1.json").read_text(encoding="utf-8"))["cases"]
    if len(ledger) != 11:
        raise ValueError("Historical case chain count differs")
    for row in ledger:
        source = ROOT / row["source_file"]
        raw = json.loads(source.read_text(encoding="utf-8").splitlines()[row["source_line"] - 1])
        if sha256_file(source) != row["source_file_sha256"] or raw != row["raw_record"] or stable_hash(raw) != row["record_semantic_sha256"]:
            raise ValueError("Historical failure evidence chain changed")
    links = 0
    for relative in ACTIVE:
        path = ROOT / relative
        for target in re.findall(r"\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
            if target.startswith(("https://", "http://", "#")):
                continue
            clean = target.split("#", 1)[0]
            destination = (path.parent / clean).resolve()
            # The audit's own report is created only after every check succeeds.
            if not destination.exists() and destination != folder / "closeout_check.json":
                raise ValueError(f"Broken active document link: {relative}: {target}")
            links += 1
    delivery = json.loads((folder / "delivery_check.json").read_text(encoding="utf-8"))
    if not delivery["passed"] or not delivery["tests"]["passed"]:
        raise ValueError("Latest full delivery/test check did not pass")
    return {"stage": "C_development_closeout_not_formal_acceptance", "passed": True, "model_calls_this_audit": 0,
            "inventory": {"runs": inventory["run_directories"], **inventory["totals"]}, "tests": delivery["tests"],
            "additional_anchor_records_verified": anchors, "normal_route_records_verified": len(normal_rows),
            "support_evidence_replays": 30, "historical_failure_chains": 11, "active_local_links_checked": links,
            "original_dataset_unchanged": True, "independent_human_reviews": 0,
            "remaining_original_target_ids": [33, 34, 37, 41, 42], "formal_accuracy": None,
            "active_document_sha256": {name: sha256_file(ROOT / name) for name in ACTIVE}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "docs/c_work/closeout_check.json")
    args = parser.parse_args()
    result = check()
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k != "active_document_sha256"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
