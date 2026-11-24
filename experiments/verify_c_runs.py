"""Verify immutable inputs, runtime snapshots and prompt equivalence after metadata corrections."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.governance.anti_hallucination import AntiHallucination
from src.governance.retrieval import LocalRetriever
from src.utils.experiment_io import latest_records, read_records, sha256_file


def main():
    results = []
    current_corpus = ROOT / "knowledge/corpus_v3.json"
    for name in ("expanded_v3", "controls_v3"):
        run = ROOT / "docs/c_work/runs" / name
        manifest = json.loads((run / "manifest.json").read_text(encoding="utf-8"))
        contract = manifest["contract"]
        if manifest["status"] != "completed" or manifest["counts"]["errors"]:
            raise ValueError("Run is not complete")
        for file, expected in [("dataset.json", contract["dataset_sha256"]), ("corpus.json", contract["corpus_sha256"])]:
            if sha256_file(run / file) != expected:
                raise ValueError(f"Modified input snapshot: {name}/{file}")
        for file, expected in contract["runtime_sha256"].items():
            if sha256_file(run / "source_snapshot" / file) != expected:
                raise ValueError(f"Modified runtime snapshot: {name}/{file}")
        latest = latest_records(read_records(run / "records.jsonl"))
        if set(latest) != set(map(tuple, manifest["planned_records"])):
            raise ValueError("Missing/extra records")
        governance = AntiHallucination(LocalRetriever(current_corpus), **contract["config"]["retrieval"])
        for row in latest.values():
            prepared = governance.prepare(row["question"], row["mode"], row["category"])
            if row["prompt"] != prepared["prompt"]:
                raise ValueError(f"Current corpus changes a model prompt: {name} {row['id']} {row['mode']}")
            before = [(h["id"], h["text"], h["source"]["url"]) for h in row["evidence"]]
            after = [(h["id"], h["text"], h["source"]["url"]) for h in prepared["evidence"]]
            if before != after:
                raise ValueError("Evidence text/order/URL changed")
        results.append({"run": name, "records": len(latest), "input_snapshots_verified": True,
                        "runtime_snapshots_verified": True, "current_corpus_prompt_equivalence": True,
                        "original_corpus_sha256": contract["corpus_sha256"],
                        "current_corpus_sha256": sha256_file(current_corpus)})
    path = ROOT / "docs/c_work/run_verification.json"
    path.write_text(json.dumps({"runs": results, "note": "v3.1修正单条出版日期元数据；428条prompt和证据正文、顺序、URL逐条相同，未重写历史结果。"}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
