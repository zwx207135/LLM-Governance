"""C's development ablations; never pass benchmark reference answers to the model."""
import argparse
import hashlib
import json
import platform
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.governance.anti_hallucination import AntiHallucination, MODES
from src.governance.retrieval import LocalRetriever


def digest(path):
    checksum = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            checksum.update(block)
    return checksum.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default=str(ROOT / "configs/c_hallucination.json"))
    parser.add_argument("--output", required=True, help="New run directory; never overwrite existing runs")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--modes", nargs="+", choices=MODES)
    args = parser.parse_args()
    config_path = Path(args.config).resolve()
    config = json.loads(config_path.read_text(encoding="utf-8"))
    dataset_path = ROOT / config["dataset"]
    corpus_path = ROOT / config["corpus"]
    items = json.loads(dataset_path.read_text(encoding="utf-8"))["items"]
    selected = set(config["development_ids"])
    if len(selected) != len(config["development_ids"]):
        raise ValueError("Duplicate development IDs")
    items = [x for x in items if x["id"] in selected]
    if len(items) != len(selected):
        raise ValueError("Unknown development IDs")
    retriever = LocalRetriever(corpus_path)
    governance = AntiHallucination(retriever, **config["retrieval"])
    modes = args.modes or config["modes"]
    if not modes or any(m not in MODES for m in modes) or len(modes) != len(set(modes)):
        raise ValueError("Invalid or duplicate modes")
    output = Path(args.output).resolve()
    output.mkdir(parents=True, exist_ok=False)
    for name, source in [("config.json", config_path), ("dataset.json", dataset_path), ("corpus.json", corpus_path)]:
        (output / name).write_bytes(source.read_bytes())
    model_path = ROOT / config["model_path"]
    model_files = {str(p.relative_to(model_path)): digest(p) for p in sorted(model_path.glob("*.json"))}
    if not args.dry_run:
        model_files.update({str(p.relative_to(model_path)): digest(p) for p in sorted(model_path.glob("*.safetensors"))})
    try:
        revision = subprocess.check_output(["git", "-c", f"safe.directory={ROOT.as_posix()}", "-C", str(ROOT), "rev-parse", "HEAD"], text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        revision = None
    code_hashes = {str(p.relative_to(ROOT)): digest(p) for folder in (ROOT / "src", ROOT / "experiments") for p in sorted(folder.rglob("*.py"))}
    for relative_path in code_hashes:
        snapshot = output / "source_snapshot" / relative_path
        snapshot.parent.mkdir(parents=True, exist_ok=True)
        snapshot.write_bytes((ROOT / relative_path).read_bytes())
    manifest = {"started_at": datetime.now(timezone.utc).isoformat(), "stage": "development_only",
                "dry_run": args.dry_run, "config": config, "modes": modes, "dataset_sha256": digest(dataset_path),
                "corpus_sha256": retriever.sha256, "revision": revision, "code_sha256": code_hashes,
                "model_config_sha256": model_files, "python": platform.python_version(), "status": "running"}
    def save_manifest():
        (output / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    save_manifest()
    model = None
    torch = None
    try:
        if not args.dry_run:
            import torch
            import transformers
            from transformers import set_seed
            from src.models.llm_model import LLMModel
            set_seed(config["seed"])
            start = time.perf_counter()
            model = LLMModel(str(model_path))
            if torch.cuda.is_available():
                torch.cuda.synchronize()
            manifest.update(model_load_seconds=time.perf_counter() - start, torch=torch.__version__,
                            transformers=transformers.__version__, device=model.device)
            model.generate("你好", max_new_tokens=8, do_sample=False)
            if torch.cuda.is_available():
                torch.cuda.synchronize()
            save_manifest()
        errors = 0
        with (output / "records.jsonl").open("w", encoding="utf-8") as stream:
            for item in items:
                for mode in modes:
                    start_prepare = time.perf_counter()
                    prepared = governance.prepare(item["question"], mode, item["category"])
                    prepare_seconds = time.perf_counter() - start_prepare
                    row = {"id": item["id"], "category": item["category"], "question": item["question"],
                           **prepared, "answer": None, "prepare_seconds": round(prepare_seconds, 6),
                           "evaluation_status": "pending_independent_review"}
                    try:
                        if model is not None:
                            set_seed(config["seed"])
                            if torch.cuda.is_available():
                                torch.cuda.synchronize()
                            start = time.perf_counter()
                            row["answer"] = model.generate(prepared["prompt"], **config["generation"])
                            if torch.cuda.is_available():
                                torch.cuda.synchronize()
                            row["generation_seconds"] = round(time.perf_counter() - start, 6)
                            row.update(model.last_generation)
                        row["status"] = "prepared" if args.dry_run else "ok"
                    except Exception as exc:
                        errors += 1
                        row.update(status="error", error=f"{type(exc).__name__}: {exc}")
                    stream.write(json.dumps(row, ensure_ascii=False) + "\n")
                    stream.flush()
                    print(f"{item['id']} {mode} {row['status']}", flush=True)
        manifest.update(status="completed_with_errors" if errors else "completed", errors=errors,
                        record_count=len(items) * len(modes), finished_at=datetime.now(timezone.utc).isoformat())
        save_manifest()
        if errors:
            raise SystemExit(1)
    except BaseException as exc:
        if manifest["status"] == "running":
            manifest.update(status="interrupted" if isinstance(exc, KeyboardInterrupt) else "failed", error=str(exc))
            save_manifest()
        raise


if __name__ == "__main__":
    main()
