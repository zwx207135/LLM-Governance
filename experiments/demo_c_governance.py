"""Run arbitrary questions without references; preserve a resumable demonstration transcript."""
import argparse
import json
import platform
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.governance.retrieval import LocalRetriever
from src.governance.service import GovernanceService, STRATEGIES
from src.utils.experiment_io import RunLedger, sha256_file

RUNTIME = ["experiments/demo_c_governance.py", "src/governance/service.py", "src/governance/retrieval.py",
           "src/governance/anti_hallucination.py", "src/governance/evidence_policy.py",
           "src/models/llm_model.py", "src/utils/experiment_io.py"]


def validate_items(items):
    if not isinstance(items, list) or not items:
        raise ValueError("Provide a nonempty items list")
    seen = set()
    for item in items:
        if not isinstance(item, dict) or set(item) - {"id", "question", "category"}:
            raise ValueError("Demo accepts only id, question and optional category; no reference or scoring fields")
        if not isinstance(item.get("id"), (str, int)) or not str(item["id"]).strip() or str(item["id"]) in seen:
            raise ValueError("Unique nonempty sample IDs required")
        if not isinstance(item.get("question"), str) or not item["question"].strip():
            raise ValueError("Nonempty questions required")
        if item.get("category") is not None and not isinstance(item["category"], str):
            raise ValueError("Category must be text")
        seen.add(str(item["id"]))
    return items


def write_transcript(ledger):
    from experiments.report_c_suite import fenced
    lines = ["# C 现场演示记录", "", "这是功能演示，不作为独立评测结果。程序拒答与模型生成分别记录；首条模型调用包含首次推理开销，不能与正式预热实验比较时延。", ""]
    for key in ledger.planned:
        row = ledger.latest.get(key)
        if row is None:
            continue
        lines.extend([f"## {row['id']} / {row['mode']}", "", row["question"], "",
                      f"状态：{row['status']}；来源：{row.get('answer_origin', 'error')}；检索：{row.get('retrieval_status', 'unknown')}。", "",
                      fenced(row.get("answer") or row.get("error") or "仅准备提示，未生成回答。"), ""])
        for hit in row.get("evidence", []):
            lines.extend([f"资料 {hit['id']}：{hit['text']}", f"来源：{hit['source']['url']}", ""])
    (ledger.directory / "transcript.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    inputs = parser.add_mutually_exclusive_group(required=True)
    inputs.add_argument("--question")
    inputs.add_argument("--input", type=Path)
    parser.add_argument("--category", default="general")
    parser.add_argument("--strategies", nargs="+", choices=STRATEGIES, default=["combined"])
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--corpus", type=Path, default=ROOT / "knowledge/corpus_v3.json")
    parser.add_argument("--model", type=Path, default=ROOT / "models/Qwen2.5-0.5B-Instruct")
    parser.add_argument("--max-new-tokens", type=int, default=192)
    parser.add_argument("--prepare-only", action="store_true")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--retry-errors", action="store_true")
    args = parser.parse_args()
    if not 1 <= args.max_new_tokens <= 2048 or len(set(args.strategies)) != len(args.strategies):
        parser.error("Use distinct strategies and 1..2048 new tokens")
    items = validate_items(json.loads(args.input.read_text(encoding="utf-8"))["items"] if args.input else
                           [{"id": "Q1", "question": args.question, "category": args.category}])
    contract = {"purpose": "demonstration_not_evaluation", "items": items, "strategies": args.strategies,
                "prepare_only": args.prepare_only, "max_new_tokens": args.max_new_tokens, "python": platform.python_version(),
                "corpus_sha256": sha256_file(args.corpus), "runtime_sha256": {p: sha256_file(ROOT / p) for p in RUNTIME},
                "model_path": str(args.model.resolve()), "seed": 20261122,
                "model_sha256": {} if args.prepare_only else {p.name: sha256_file(p) for p in args.model.glob("*") if p.suffix in (".json", ".txt", ".safetensors")}}
    ledger = RunLedger(args.output, contract, [(str(i["id"]), s) for i in items for s in args.strategies], args.resume)
    if not args.resume:
        (args.output / "corpus.json").write_bytes(args.corpus.read_bytes())
        for relative in RUNTIME:
            path = args.output / "source_snapshot" / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes((ROOT / relative).read_bytes())
    elif sha256_file(args.output / "corpus.json") != contract["corpus_sha256"]:
        raise ValueError("Stored corpus snapshot changed")

    def factory():
        import torch
        import transformers
        from transformers import set_seed
        from src.models.llm_model import LLMModel
        set_seed(contract["seed"])
        model = LLMModel(str(args.model), local_files_only=True)
        ledger.manifest.update(torch=torch.__version__, transformers=transformers.__version__, device=model.device)
        ledger.save()
        return model

    def synchronize():
        if "torch" in sys.modules and sys.modules["torch"].cuda.is_available():
            sys.modules["torch"].cuda.synchronize()

    service = GovernanceService(LocalRetriever(args.corpus), factory, synchronize)
    by_id = {str(i["id"]): i for i in items}
    ledger.manifest.update(status="running", stage="demonstration_not_evaluation")
    ledger.save()
    try:
        for ident, strategy in ledger.pending(args.retry_errors):
            item = by_id[ident]
            row = {"id": item["id"], "mode": strategy, "question": item["question"], "category": item.get("category")}
            try:
                row.update(service.answer(item["question"], strategy, item.get("category"), args.max_new_tokens, args.prepare_only))
            except Exception as exc:
                row.update(status="error", error=f"{type(exc).__name__}: {exc}")
            ledger.append(row)
            print(json.dumps({k: row.get(k) for k in ("id", "mode", "status", "answer_origin", "answer", "error")}, ensure_ascii=False), flush=True)
        ledger.manifest["status"] = "completed_with_errors" if ledger.manifest["counts"]["errors"] else "completed"
        ledger.save()
        write_transcript(ledger)
        if ledger.manifest["counts"]["errors"]:
            raise SystemExit(1)
    except BaseException:
        if ledger.manifest["status"] == "running":
            ledger.manifest["status"] = "interrupted"
            ledger.save()
        write_transcript(ledger)
        raise


if __name__ == "__main__":
    main()
