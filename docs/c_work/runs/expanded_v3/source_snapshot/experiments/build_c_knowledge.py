"""Build a reproducible curated corpus; benchmark files are not ingestion inputs."""
import hashlib
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN = {"question", "reference", "reference_source", "answer", "score", "rationale"}


def validate_document(doc):
    if FORBIDDEN.intersection(doc):
        raise ValueError("Benchmark/score fields must not enter the knowledge builder")
    if not doc.get("url", "").startswith("https://") or not doc.get("locator"):
        raise ValueError("An HTTPS source URL and locator are required")
    date.fromisoformat(doc["accessed_at"])
    if doc.get("published_at"):
        date.fromisoformat(doc["published_at"])
    if not doc.get("paragraphs"):
        raise ValueError("Document has no paragraphs")
    for p in doc["paragraphs"]:
        if FORBIDDEN.intersection(p) or not p.get("text", "").strip() or not p.get("topics"):
            raise ValueError("A paragraph must contain source prose and topic anchors only")


def build(base, documents):
    # The base is an already curated source corpus, not the answer-verification registry.
    sources = list(base["sources"])
    chunks = list(base["chunks"])
    for doc in documents["documents"]:
        validate_document(doc)
        sources.append({k: v for k, v in doc.items() if k != "paragraphs"})
        for paragraph in doc["paragraphs"]:
            if len(paragraph["text"]) > 500:
                raise ValueError("Split long paragraphs at semantic boundaries before ingestion")
            chunks.append({**paragraph, "source_id": doc["id"], "text_sha256": hashlib.sha256(paragraph["text"].encode()).hexdigest()})
    for collection in (sources, chunks):
        if len({x["id"] for x in collection}) != len(collection):
            raise ValueError("Duplicate source or chunk ID")
    return {"version": "c-dev-2026-11-22-v3", "purpose": "开发用主题知识库，不宣称与现有题集主题独立。",
            "selection_policy": documents["scope"], "sources": sources, "chunks": chunks}


def main():
    base_path = ROOT / "knowledge/corpus.json"
    docs_path = ROOT / "knowledge/source_documents.json"
    corpus = build(json.loads(base_path.read_text(encoding="utf-8")), json.loads(docs_path.read_text(encoding="utf-8")))
    target = ROOT / "knowledge/corpus_v3.json"
    target.write_text(json.dumps(corpus, ensure_ascii=False, indent=2), encoding="utf-8")
    manifest = {"version": corpus["version"], "source_count": len(corpus["sources"]), "chunk_count": len(corpus["chunks"]),
                "inputs": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in (base_path, docs_path)},
                "corpus_sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
                "chunking": "人工按语义分段，每段不超过500字符；运行时以固定中文二元字符词元构建BM25索引"}
    (ROOT / "knowledge/build_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
