"""Package C's sources, evidence and real runs; omit model weights and local caches."""
import argparse
import hashlib
import json
import zipfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
RUNS = ("expanded_v3", "controls_v3", "policy_comparison_v1", "demo_v1", "source_bound_v1", "structured_v1", "structured_prepare_v1",
        "balanced_materials_v1", "balanced_labels_cn_v1", "balanced_prepare_v1", "joint_batch_v1", "joint_batch_prepare_v1", "normal_route_v1",
        "anchor_diagnostics_v1", "evidence_first_v1", "nobel_scope_v1", "nobel_scope_followup_v1", "nobel_scope_followup_v2",
        "evidence_binding_v1", "year_alias_v1", "subject_focus_v1")


def verify_archive(path):
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)):
            raise ValueError("Duplicate archive paths")
        for name in names:
            p = PurePosixPath(name)
            if p.is_absolute() or ".." in p.parts or "\\" in name:
                raise ValueError("Invalid archive path")
        manifest = json.loads(archive.read("C_RELEASE_MANIFEST.json"))
        if set(names) != set(manifest["files"]) | {"C_RELEASE_MANIFEST.json"}:
            raise ValueError("Archive contents differ from manifest")
        for name, expected in manifest["files"].items():
            if hashlib.sha256(archive.read(name)).hexdigest() != expected:
                raise ValueError(f"Checksum mismatch: {name}")
        return {"verified_files": len(manifest["files"]), "stage": manifest["stage"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--verify", type=Path)
    args = parser.parse_args()
    if args.verify:
        print(json.dumps(verify_archive(args.verify), ensure_ascii=False))
        return
    if not args.output:
        parser.error("Provide --output or --verify")
    if args.output.exists():
        raise FileExistsError("Use a new release filename")
    for run in RUNS:
        manifest = json.loads((ROOT / "docs/c_work/runs" / run / "manifest.json").read_text(encoding="utf-8"))
        if manifest["status"] != "completed" or manifest["counts"]["missing"] or manifest["counts"]["errors"]:
            raise ValueError(f"Run {run} is not complete")
    files = []
    for folder in ("src", "experiments", "tests", "configs", "knowledge", "datasets"):
        files.extend(p for p in (ROOT / folder).rglob("*") if p.is_file() and p.suffix in (".py", ".json", ".md"))
    documents = ROOT / "docs/c_work"
    files.extend(p for p in documents.rglob("*") if p.is_file() and "runs" not in p.relative_to(documents).parts and
                 (p.suffix in (".py", ".md", ".json", ".csv", ".png", ".svg", ".xlsx", ".mjs", ".pptx", ".bib") or
                  p.suffix == ".txt" and p.name.startswith("requirements-c-") or
                  p.suffix == ".log" and any(part.startswith("assignment_check_") for part in p.relative_to(documents).parts)))
    for run in (*RUNS, "joint_smoke_v1"):
        files.extend(p for p in (documents / "runs" / run).rglob("*") if p.is_file() and p.suffix in (".py", ".json", ".jsonl", ".md", ".csv", ".png"))
    files.extend(p for p in (ROOT / "README.md", ROOT / ".gitignore", ROOT / ".gitattributes", ROOT / "C_PROGRESS.md") if p.exists())
    # The temporal case ledger binds these original baseline answers byte-for-byte.
    baseline = ROOT / "results/hallucination/results.json"
    if baseline.exists():
        files.append(baseline)
    files = sorted(set(files), key=lambda p: p.relative_to(ROOT).as_posix())
    payload = {p.relative_to(ROOT).as_posix(): p.read_bytes() for p in files}
    manifest = {"stage": "C_development_handoff_not_final_acceptance", "model_weights_included": False, "runs": list(RUNS),
                "files": {name: hashlib.sha256(data).hexdigest() for name, data in payload.items()}}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(args.output, "x", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, data in payload.items():
            archive.writestr(name, data)
        archive.writestr("C_RELEASE_MANIFEST.json", json.dumps(manifest, ensure_ascii=False, indent=2))
    result = {**verify_archive(args.output), "archive_sha256": hashlib.sha256(args.output.read_bytes()).hexdigest(),
              "bytes": args.output.stat().st_size}
    args.output.with_suffix(".sha256.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
