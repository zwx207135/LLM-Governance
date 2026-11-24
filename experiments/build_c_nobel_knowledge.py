"""Add a scoped public-source topic supplement without modifying frozen v3."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from experiments.build_c_knowledge import build
from src.governance.retrieval import LocalRetriever
from src.utils.experiment_io import sha256_file


def main():
    base_path = ROOT / "knowledge/corpus_v3.json"
    docs_path = ROOT / "knowledge/nobel_documents_v1.json"
    base = json.loads(base_path.read_text(encoding="utf-8"))
    docs = json.loads(docs_path.read_text(encoding="utf-8"))
    for doc in docs["documents"]:
        if doc["access_method"] != "indexed_body":
            raise ValueError("This supplement declares indexed access only")
        for paragraph in doc["paragraphs"]:
            scope = paragraph["scope"]
            if scope["kind"] == "award_record" and (not isinstance(scope["award_year"], int) or not scope["subject_aliases"]):
                raise ValueError("Award record requires year and subject metadata")
    result = build(base, docs)
    result.update(version="c-dev-2026-11-23-v4", selection_policy=docs["scope"],
                  base_corpus_sha256=sha256_file(base_path), supplement_version=docs["version"])
    target = ROOT / "knowledge/corpus_v4.json"
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    LocalRetriever(target)
    manifest = {"stage": "targeted_development_only", "corpus_sha256": sha256_file(target),
                "sources": len(result["sources"]), "chunks": len(result["chunks"]),
                "added_sources": len(docs["documents"]), "added_chunks": sum(len(d["paragraphs"]) for d in docs["documents"]),
                "inputs": {str(p.relative_to(ROOT)): sha256_file(p) for p in (base_path, docs_path)},
                "base_unchanged": result["sources"][:len(base["sources"])] == base["sources"] and result["chunks"][:len(base["chunks"])] == base["chunks"],
                "independent_human_review": False, "independent_holdout": False}
    (ROOT / "knowledge/build_manifest_v4.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
