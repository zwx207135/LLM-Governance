"""Verify frozen source replays and summarize targeted evidence diagnostics."""
import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUN_NAMES = ("nobel_scope_v1", "nobel_scope_followup_v1", "nobel_scope_followup_v2")


def replay(folder):
    # A fresh process imports the run's own code, including superseded policies.
    snapshot = folder / "source_snapshot"
    sys.path.insert(0, str(snapshot))
    import src.governance.anti_hallucination as anti
    import src.governance.retrieval_safe as safe
    import src.governance.retrieval_scoped as scoped
    for module in (anti, safe, scoped):
        if not Path(module.__file__).resolve().is_relative_to(snapshot.resolve()):
            raise ValueError("Replay imported working code instead of frozen snapshot")
    config = json.loads((folder / "config.json").read_text(encoding="utf-8"))
    data = json.loads((folder / "dataset.json").read_text(encoding="utf-8"))
    items = [{k: x[k] for k in ("id", "question", "category")} for x in data["items"] if x["id"] in config["existing_ids"]] + config["probes"]
    output = []
    for mode in config["corpora"]:
        implementation = scoped.AwardScopedRetriever if mode == "v4_scoped" else getattr(scoped, "AwardScopedRetrieverV2") if mode == "v4_scoped_v2" else safe.SafeAnchorRetriever
        retriever = implementation(folder / (mode + "_corpus.json"))
        gov = anti.AntiHallucination(retriever, **config["retrieval"])
        for item in items:
            prepared = gov.prepare(item["question"], "combined", item["category"])
            diagnostic = retriever.search_with_diagnostics(item["question"], **config["retrieval"])
            output.append({"id": str(item["id"]), "mode": mode, "question": item["question"], "category": item["category"],
                           **{k: prepared[k] for k in ("prompt", "evidence", "retrieval_status")},
                           "rejected": diagnostic["rejected"], "selection_events": diagnostic.get("selection_events", [])})
    print(json.dumps(output, ensure_ascii=False))


def verify(folder):
    sys.path.insert(0, str(ROOT))
    from src.utils.experiment_io import sha256_file, stable_hash
    manifest = json.loads((folder / "manifest.json").read_text(encoding="utf-8"))
    contract = manifest["contract"]
    if manifest["status"] != "completed" or stable_hash(contract) != manifest["contract_sha256"]:
        raise ValueError("Run incomplete or contract changed")
    for name, expected in contract["inputs_sha256"].items():
        if sha256_file(folder / name) != expected:
            raise ValueError("Input snapshot changed: " + name)
    for name, expected in contract["runtime_sha256"].items():
        if sha256_file(folder / "source_snapshot" / name) != expected:
            raise ValueError("Code snapshot changed: " + name)
    rows = [json.loads(l) for l in (folder / "records.jsonl").read_text(encoding="utf-8").splitlines()]
    keys = {(str(r["id"]), r["mode"]) for r in rows}
    if len(keys) != len(rows) or keys != {tuple(x) for x in manifest["planned_records"]}:
        raise ValueError("Unexpected/duplicate sample")
    if any(r["status"] != "ok" or r.get("model_calls") != 1 or r.get("answer_origin") != "model" for r in rows):
        raise ValueError("Expected real successful model outputs")
    result = subprocess.run([sys.executable, "-X", "utf8", str(Path(__file__).resolve()), "--replay-snapshot", str(folder.resolve())],
                            capture_output=True, text=True, encoding="utf-8", timeout=30, check=True)
    expected_rows = {(r["id"], r["mode"]): r for r in json.loads(result.stdout)}
    if set(expected_rows) != keys:
        raise ValueError("Planned records do not match frozen inputs")
    for row in rows:
        expected = expected_rows[str(row["id"]), row["mode"]]
        if any(row[k] != value for k, value in expected.items() if k != "id"):
            raise ValueError("Raw record differs from frozen question-only preparation")
    return manifest, rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--replay-snapshot", type=Path)
    args = parser.parse_args()
    if args.replay_snapshot:
        replay(args.replay_snapshot)
        return
    sys.path.insert(0, str(ROOT))
    from src.utils.experiment_io import sha256_file
    folder = ROOT / "docs/c_work"
    runs = {name: verify(folder / "runs" / name) for name in RUN_NAMES}
    first = runs[RUN_NAMES[0]][0]["contract"]
    for manifest, _ in runs.values():
        contract = manifest["contract"]
        if contract["model_sha256"] != first["model_sha256"]:
            raise ValueError("Model differs across paired conditions")
        for key in ("existing_ids", "probes", "generation", "seed", "retrieval"):
            if contract["config"][key] != first["config"][key]:
                raise ValueError("Paired question/configuration differs")
        for key in ("dataset.json", "documents.json"):
            if contract["inputs_sha256"][key] != first["inputs_sha256"][key]:
                raise ValueError("Paired frozen input differs")
    comparisons = []
    for ident in [str(x) for x in first["config"]["existing_ids"]] + [x["id"] for x in first["config"]["probes"]]:
        comparisons.append({"id": ident, "conditions": [{"run": name, "record": row} for name, (_, rows) in runs.items() for row in rows if str(row["id"]) == ident]})
    summary = {"stage": "targeted_development_not_independent_test", "independent_human_reviews": 0, "factual_accuracy": None,
               "total_model_calls": sum(len(rows) for _, rows in runs.values()), "runs": {},
               "prototype_followup_retained": "nobel_scope_followup_v1", "final_exploratory_candidate": "AwardScopedRetrieverV2 in nobel_scope_followup_v2",
               "corpus_sources": 21, "corpus_chunks": 31, "added_sources": 5, "added_chunks": 6,
               "old_corpus_sha256": sha256_file(ROOT / "knowledge/corpus_v3.json")}
    for name, (manifest, rows) in runs.items():
        summary["runs"][name] = {"records": len(rows), "truncated": sum(r["truncated"] for r in rows),
                                  "records_sha256": sha256_file(folder / "runs" / name / "records.jsonl"),
                                  "frozen_prompt_replays_verified": len(rows),
                                  "rejected_candidates": sum(len(r["rejected"]) for r in rows)}
    # Report the full failed prototype too; no selecting only favourable outputs.
    (folder / "nobel_scope_comparison.json").write_text(json.dumps(comparisons, ensure_ascii=False, indent=2), encoding="utf-8")
    (folder / "nobel_scope_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
