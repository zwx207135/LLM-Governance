"""C development evidence-use report, with frozen-code prompt replay."""
import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNS = ("subject_focus_v1",)


def replay(folder):
    snapshot = folder / "source_snapshot"
    sys.path.insert(0, str(snapshot))
    import experiments.run_c_subject_focus as runner
    import src.governance.subject_focus as binding
    from src.governance.retrieval_scoped import AwardScopedRetrieverV2
    for module in (runner, binding):
        if not Path(module.__file__).resolve().is_relative_to(snapshot.resolve()):
            raise ValueError("Working source imported instead of frozen runtime")
    config = json.loads((folder / "config.json").read_text(encoding="utf-8"))
    data, controls = [json.loads((folder / (key + ".json")).read_text(encoding="utf-8")) for key in ("dataset", "controls")]
    implementation = AwardScopedRetrieverV2
    if config.get("retriever_version") == "year_alias":
        from src.governance.retrieval_year_alias import AwardYearAliasRetriever
        implementation = AwardYearAliasRetriever
    retriever = implementation(folder / "corpus.json")
    policy = binding.SubjectFocusPolicy(retriever, **config["retrieval"])
    output = []
    for item in runner.prepare_items(config, data, controls):
        for mode in binding.POLICIES:
            row = {**item, **policy.prepare(item["question"], mode, item["category"])}
            if config.get("retriever_version") == "year_alias":
                row["retrieval_diagnostics"] = retriever.search_with_diagnostics(item["question"], **config["retrieval"])
            output.append(row)
    print(json.dumps(output, ensure_ascii=False))


def verify(folder):
    sys.path.insert(0, str(ROOT))
    from src.utils.experiment_io import sha256_file, stable_hash
    manifest = json.loads((folder / "manifest.json").read_text(encoding="utf-8"))
    contract = manifest["contract"]
    if manifest["status"] != "completed" or stable_hash(contract) != manifest["contract_sha256"]:
        raise ValueError("Incomplete run or modified contract")
    for name, expected in contract["inputs_sha256"].items():
        if sha256_file(folder / name) != expected:
            raise ValueError("Input snapshot changed: " + name)
    for name, expected in contract["runtime_sha256"].items():
        if sha256_file(folder / "source_snapshot" / name) != expected:
            raise ValueError("Runtime snapshot changed: " + name)
    rows = [json.loads(line) for line in (folder / "records.jsonl").read_text(encoding="utf-8").splitlines()]
    keyed = {(str(r["id"]), r["mode"]): r for r in rows}
    if len(keyed) != len(rows) or set(keyed) != {tuple(x) for x in manifest["planned_records"]}:
        raise ValueError("Unexpected or duplicate records")
    if any(r["status"] != "ok" or r["model_calls"] != 1 or r["answer_origin"] != "model" for r in rows):
        raise ValueError("Expected real model outputs")
    result = subprocess.run([sys.executable, "-X", "utf8", str(Path(__file__).resolve()), "--replay", str(folder.resolve())],
                            capture_output=True, text=True, encoding="utf-8", timeout=30, check=True)
    expected_rows = {(str(r["id"]), r["mode"]): r for r in json.loads(result.stdout)}
    if set(expected_rows) != set(keyed):
        raise ValueError("Frozen plan differs from inputs")
    for key, expected in expected_rows.items():
        if any(keyed[key][field] != value for field, value in expected.items()):
            raise ValueError("Question-only prompt/evidence replay differs: " + str(key))
    for ident, mode in keyed:
        if mode == "combined" and keyed[ident, mode]["evidence"] != keyed[ident, "subject_focus"]["evidence"]:
            raise ValueError("Rendering comparison changed retrieval evidence")
    return manifest, keyed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--replay", type=Path)
    args = parser.parse_args()
    if args.replay:
        replay(args.replay)
        return
    sys.path.insert(0, str(ROOT))
    from src.utils.experiment_io import sha256_file
    folder = ROOT / "docs/c_work"
    summary = {"scope": "C_method_diagnostics_only", "independent_human_reviews": 0, "formal_accuracy": None, "runs": {}}
    comparisons = []
    for name in RUNS:
        manifest, keyed = verify(folder / "runs" / name)
        ids = [ident for ident, mode in keyed if mode == "combined"]
        controls = [i for i in ids if keyed[i, "combined"]["category"] == "normal_control"]
        summary["runs"][name] = {
            "model_calls": len(keyed), "pairs": len(ids), "same_evidence_pairs": len(ids),
            "focus_applied_pairs": sum(keyed[i, "subject_focus"]["subject_focus_applied"] for i in ids),
            "changed_answers": sum(keyed[i, "combined"]["answer"] != keyed[i, "subject_focus"]["answer"] for i in ids),
            "truncated": sum(r["truncated"] for r in keyed.values()), "normal_control_pairs": len(controls),
            "normal_same_prompt_pairs": sum(keyed[i, "combined"]["prompt"] == keyed[i, "subject_focus"]["prompt"] for i in controls),
            "normal_same_answer_pairs": sum(keyed[i, "combined"]["answer"] == keyed[i, "subject_focus"]["answer"] for i in controls),
            "records_sha256": sha256_file(folder / "runs" / name / "records.jsonl"), "frozen_replays_verified": len(keyed)}
        comparisons.extend({"run": name, "id": ident, "combined": keyed[ident, "combined"], "subject_focus": keyed[ident, "subject_focus"]} for ident in ids)
    summary["total_model_calls"] = sum(r["model_calls"] for r in summary["runs"].values())
    from src.governance.retrieval_scoped import AwardScopedRetrieverV2
    from src.governance.retrieval_year_alias import AwardYearAliasRetriever
    corpus = ROOT / "knowledge/corpus_v4.json"
    old, new = AwardScopedRetrieverV2(corpus), AwardYearAliasRetriever(corpus)
    originals = json.loads((ROOT / "datasets/hallucination/test_set.json").read_text(encoding="utf-8"))["items"]
    summary["year_alias_regression_checked_questions"] = len(originals)
    summary["year_alias_regression_changed_ids"] = [x["id"] for x in originals if old.search(x["question"]) != new.search(x["question"])]
    (folder / "subject_focus_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    (folder / "subject_focus_comparison.json").write_text(json.dumps(comparisons, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
