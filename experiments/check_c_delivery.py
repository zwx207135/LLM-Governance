"""Check C's completed development artifacts without generating new model answers."""
import argparse
import contextlib
import csv
import io
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from experiments import verify_c_demo, verify_c_policy_comparison, verify_c_runs
from experiments.evaluate_c_reviews import load_and_validate
from experiments.check_c_source_bound import mode_tables, score_records
from experiments.report_c_policy_comparison import load_comparison
from experiments.report_c_source_followup import validate_followup
from experiments.report_c_structured import analyze as analyze_structured
from experiments.report_c_balanced_materials import analyze_balanced
from experiments.compare_c_material_labels import compare_runs
from experiments.verify_c_integration import verify as verify_integration
from experiments.report_c_joint_batch import analyze as analyze_joint_batch
from experiments.report_c_nobel_comparison import verify as verify_nobel
from experiments.report_c_evidence_binding import verify as verify_binding
from experiments.build_c_pending_repairs import verify as verify_pending_repairs
from experiments.build_c_revision_index import verify as verify_revision_index
from experiments.check_c_component_contract import check as check_component
from experiments.report_c_subject_focus import verify as verify_subject_focus
from experiments.check_c_pilot_review import check as check_pilot
from src.evaluation.review_metrics import fingerprint
from src.governance.evidence_policy import EvidencePolicy
from src.governance.retrieval import LocalRetriever
from src.evaluation.reconciliation import reconcile
from src.utils.experiment_io import latest_records, read_records, sha256_file


def verify_review_state(folder):
    manifest = json.loads((folder / "manifest.json").read_text(encoding="utf-8"))
    for name, expected in manifest["runtime_sha256"].items():
        if sha256_file(folder / "source_snapshot" / name) != expected:
            raise ValueError("Modified reconciliation runtime snapshot")
    inputs = []
    for item in manifest["annotation_inputs"]:
        path = folder / item["snapshot"]
        if sha256_file(path) != item["sha256"]:
            raise ValueError("Modified original review snapshot")
        inputs.append(path)
    state = json.loads((folder / "review_state.json").read_text(encoding="utf-8"))
    # This artifact deliberately proves that AI-only inputs yield no human results.
    if manifest["decisions_sha256"] is not None:
        raise ValueError("The AI-only verification artifact must not contain human decisions")
    rebuilt = reconcile(load_and_validate(inputs))
    if state != rebuilt or state["report"]["human_judgment_records"] != 0 or state["report"]["tables"]:
        raise ValueError("Review status differs from its declared AI-only inputs")
    with (folder / "adjudication_blank.csv").open(encoding="utf-8-sig", newline="") as stream:
        if list(csv.DictReader(stream)):
            raise ValueError("No invented human conflicts should appear for AI-only inputs")
    return {"original_judgments": state["report"]["ai_judgments_excluded"], "human_judgments": 0,
            "resolved_answers": 0, "runtime_and_input_snapshots_verified": True,
            "seven_dimension_agreement_unavailable": all(v["n"] == 0 and v["kappa"] is None
                                                       for v in state["report"]["agreement_before_adjudication"].values())}


def verify_followup(folder):
    report_folder = folder / "source_followup_v1"
    manifest = json.loads((report_folder / "manifest.json").read_text(encoding="utf-8"))
    for name, expected in manifest["unchanged_frozen_inputs"].items():
        if sha256_file(ROOT / name) != expected:
            raise ValueError("Follow-up unexpectedly changed frozen development input: " + name)
    if sha256_file(report_folder / "source_snapshot.json") != manifest["followup_sha256"] or sha256_file(folder / "source_followup_v1.json") != manifest["followup_sha256"]:
        raise ValueError("Follow-up source ledger changed; publish a separate version")
    payload = json.loads((report_folder / "source_snapshot.json").read_text(encoding="utf-8"))
    counts = validate_followup(payload, json.loads((folder / "data_audit.json").read_text(encoding="utf-8")))
    run = folder / "runs/source_bound_v1"
    run_manifest, rows = load_comparison(run)
    for name, expected in run_manifest["contract"]["runtime_sha256"].items():
        if sha256_file(run / "source_snapshot" / name) != expected:
            raise ValueError("Modified diagnostic generation source snapshot")
    controls = json.loads((run / "controls.json").read_text(encoding="utf-8"))
    saved = json.loads((run / "source_bound_checks.json").read_text(encoding="utf-8"))
    policy = EvidencePolicy(LocalRetriever(run / "corpus.json"), **run_manifest["contract"]["config"]["retrieval"])
    if len(rows) != 15 or any(r["answer_origin"] != "model" or r["model_calls"] != 1 for r in rows):
        raise ValueError("Expected fifteen real supplied-material diagnostic model answers")
    for row in rows:
        if row["prompt"] != policy.prepare(row["question"], row["mode"], row["category"])["prompt"]:
            raise ValueError("Diagnostic prompt is not derived from question and policy alone")
    scored = score_records(rows, controls["items"])
    if scored != saved["checks"] or mode_tables(scored) != saved["modes"]:
        raise ValueError("Saved diagnostic checks differ from frozen questions/answers")
    if sha256_file(run / saved["grader_snapshot"]) != saved["grader_sha256"]:
        raise ValueError("Diagnostic evaluation code snapshot changed")
    return {"items_followed_up": manifest["items"], "sources": manifest["sources"], "dispositions": counts,
            "frozen_inputs_unchanged": True, "diagnostic_records": len(rows), "model_generated_answers": len(rows),
            "diagnostics_separate_from_original_entity_truth": True, "prompt_and_grading_snapshots_verified": True}


def verify_structured(folder):
    run = folder / "runs/structured_v1"
    result, rows = analyze_structured(run)
    saved = json.loads((run / "structured_checks.json").read_text(encoding="utf-8"))
    if {k: v for k, v in saved.items() if k != "evaluation_sources"} != result:
        raise ValueError("Structured report differs from frozen raw outputs")
    for name, expected in saved["evaluation_sources"].items():
        if sha256_file(run / name) != expected:
            raise ValueError("Structured evaluation source snapshot changed")
    constrained = [r for r in result["checks"] if r["decoder"] == "json"]
    if len(rows) != 30 or len(constrained) != 15 or not all(r["schema_conformant"] for r in constrained):
        raise ValueError("Expected thirty real answers and fifteen schema-conformant constrained outputs")
    dry_run = folder / "runs/structured_prepare_v1"
    dry_manifest = json.loads((dry_run / "manifest.json").read_text(encoding="utf-8"))
    dry_rows = latest_records(read_records(dry_run / "records.jsonl"))
    if dry_manifest["status"] != "completed" or len(dry_rows) != 30 or any(r["status"] != "prepared" or r["answer"] is not None for r in dry_rows.values()):
        raise ValueError("Preparation recovery must not be counted as model answers")
    return {"model_generated_answers": 30, "constrained_outputs": 15,
            "schema_conformant": sum(r["schema_conformant"] for r in constrained),
            "all_six_semantic_combinations_retained": all(n == 6 for n in result["all_declared_combinations_per_task"].values()),
            "same_prompt_and_answer_free_replays": result["free_replay"]["same_answer"],
            "prompt_and_runtime_snapshots_verified": True, "preparation_records_not_answers": len(dry_rows),
            "formal_winner_selected": False}


def verify_balanced_materials(folder):
    runs = [folder / "runs" / name for name in ("balanced_materials_v1", "balanced_labels_cn_v1")]
    for run in runs:
        actual, rows = analyze_balanced(run)
        saved = json.loads((run / "balanced_checks.json").read_text(encoding="utf-8"))
        if {k: v for k, v in saved.items() if k not in ("evaluation_sources", "figure")} != actual:
            raise ValueError("Balanced material report differs from frozen answers")
        if len(rows) != 192 or actual["allowed_semantic_combinations"] != [9]:
            raise ValueError("Expected full balanced diagnostic with all nine choices")
        for name, expected in saved["evaluation_sources"].items():
            if sha256_file(run / name) != expected:
                raise ValueError("Balanced evaluation source snapshot changed")
        if sha256_file(run / saved["figure"]["path"]) != saved["figure"]["sha256"]:
            raise ValueError("Balanced confusion matrix changed")
    comparison = compare_runs(*runs)
    saved = json.loads((folder / "material_label_comparison.json").read_text(encoding="utf-8"))
    if {k: v for k, v in saved.items() if k != "input_record_sha256"} != comparison:
        raise ValueError("Label comparison is not tied to the paired original runs")
    for run in runs:
        if sha256_file(run / "records.jsonl") != saved["input_record_sha256"][run.name]:
            raise ValueError("Compared raw output file changed")
    packet = folder / "review_packet_materials_v1"
    mapping = json.loads((folder / "review_packet_materials_v1_mapping.json").read_text(encoding="utf-8"))
    if len(mapping) != 96:
        raise ValueError("Expected 96 additional blank review items")
    raw = {run.name: latest_records(read_records(run / "records.jsonl")) for run in runs}
    for item in mapping.values():
        if fingerprint(raw[item["run"]][(str(item["id"]), item["mode"])]) != item["content_sha256"]:
            raise ValueError("Review item refers to a changed answer")
    for reviewer in ("C", "D"):
        with (packet / f"annotator_{reviewer}_blank.csv").open(encoding="utf-8-sig", newline="") as stream:
            blank = list(csv.DictReader(stream))
        if {r["review_id"] for r in blank} != set(mapping) or any(value for r in blank for key, value in r.items() if key != "review_id"):
            raise ValueError("Material reviewer templates must remain blank and complete")
    return {"model_generated_answers": 384, "runs": [r.name for r in runs], "related_topics": 8,
            "unique_claims": 24, "position_variants": 48, "label_followup_is_exploratory": True,
            "external_retrieved_passages": 0, "schema_combinations_retained": 9,
            "material_claim_and_generation_pairing_verified": True, "confusion_figures_verified": True,
            "blank_records_per_annotator": 96, "independent_human_reviews_completed": 0}


def verify_joint_batch(folder):
    run = folder / "runs/joint_batch_v1"
    actual, rows = analyze_joint_batch(run)
    saved = json.loads((run / "joint_checks.json").read_text(encoding="utf-8"))
    if saved != actual or len(rows) != 96:
        raise ValueError("Joint batch report differs from raw outputs")
    dry = folder / "runs/joint_batch_prepare_v1"
    manifest = json.loads((dry / "manifest.json").read_text(encoding="utf-8"))
    prepared = latest_records(read_records(dry / "records.jsonl"))
    if manifest["status"] != "completed" or len(prepared) != 96 or any(r["status"] != "prepared" or r["answer"] is not None or r["model_calls"] for r in prepared.values()):
        raise ValueError("Dry-run recovery incorrectly contains model answers")
    return {"records": 96, "model_generated_answers": actual["model_generated_answers"],
            "program_abstentions": actual["program_abstentions"], "prepared_records_not_answers": 96,
            "input_runtime_and_audit_verified": True, "bias_effectiveness": "not_evaluated"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-tests", action="store_true")
    args = parser.parse_args()
    folder = ROOT / "docs/c_work"
    if args.run_tests:
        result = unittest.TextTestRunner(verbosity=1).run(unittest.defaultTestLoader.discover(str(ROOT / "tests")))
        checks = {"tests_run": result.testsRun, "failures": len(result.failures), "errors": len(result.errors),
                  "skipped": len(result.skipped), "passed": result.wasSuccessful()}
        (folder / "test_results.json").write_text(json.dumps(checks, ensure_ascii=False, indent=2), encoding="utf-8")
        if not result.wasSuccessful():
            raise SystemExit(1)
    else:
        checks = json.loads((folder / "test_results.json").read_text(encoding="utf-8"))
        if not checks["passed"]:
            raise ValueError("Last recorded test run did not pass")
    for verifier in (verify_c_runs.main, verify_c_policy_comparison.main, verify_c_demo.main):
        with contextlib.redirect_stdout(io.StringIO()):
            verifier()
    review = verify_review_state(folder / "reconciliation_status_v1")
    followup = verify_followup(folder)
    structured = verify_structured(folder)
    balanced = verify_balanced_materials(folder)
    integration = verify_integration()
    joint_batch = verify_joint_batch(folder)
    nobel_runs = {name: verify_nobel(folder / "runs" / name) for name in ("nobel_scope_v1", "nobel_scope_followup_v1", "nobel_scope_followup_v2")}
    nobel = {"model_generated_answers": sum(len(rows) for _, rows in nobel_runs.values()),
             "runs": list(nobel_runs), "frozen_prompt_and_evidence_replay_verified": True,
             "independent_human_reviews": 0, "factual_accuracy": None}
    binding_runs = {name: verify_binding(folder / "runs" / name) for name in ("evidence_binding_v1", "year_alias_v1")}
    binding = {"scope": "C_method_diagnostics_only", "model_generated_answers": sum(len(rows) for _, rows in binding_runs.values()),
               "frozen_prompt_and_evidence_replay_verified": True, "formal_accuracy": None}
    pending_repairs = verify_pending_repairs(folder / "pending_repairs_v2")
    revision_index = verify_revision_index(folder / "revision_index_v1")
    component_contract = check_component()
    _, subject_rows = verify_subject_focus(folder / "runs/subject_focus_v1")
    result = {"status": "development_artifacts_checked_human_review_pending", "passed": True,
              "tests_executed_this_check": args.run_tests, "tests": checks,
              "original_runs_verified": ["expanded_v3", "controls_v3", "policy_comparison_v1"],
              "development_outputs": 548, "development_model_answers": 543, "development_program_abstentions": 5,
              "separate_demo_outputs": 12, "demo_model_answers": 11, "demo_program_abstentions": 1,
              "review_workflow": review,
              "source_followup": followup,
              "structured_decoding": structured,
              "balanced_material_diagnostics": balanced,
              "joint_integration": integration,
              "joint_batch": joint_batch,
              "nobel_source_and_scope_diagnostics": nobel,
              "C_evidence_use_diagnostics": binding,
              "C1_pending_reference_repairs": pending_repairs,
              "C1_revision_index": revision_index,
              "C_component_contract": {"passed": True, "cases": len(component_contract["cases"]), "model_calls": 0},
              "C_subject_focus": {"records": len(subject_rows), "frozen_replays_verified": True, "formal_accuracy": None},
              "C_pilot_AI_draft": check_pilot(),
              "note": "No new inference; this checks development artifacts, not final acceptance or effectiveness."}
    (folder / "delivery_check.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
