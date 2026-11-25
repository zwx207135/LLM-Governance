"""Compare free and finite-schema decoding with unchanged prompts and all semantic choices."""
import argparse
import json
import platform
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.governance.evidence_policy import EvidencePolicy, POLICIES
from src.governance.finite_json import FiniteJsonConstraint, allowed_outputs
from src.governance.retrieval import LocalRetriever
from src.utils.experiment_io import RunLedger, sha256_file, stable_hash

RUNTIME = ["experiments/run_c_structured_comparison.py", "src/governance/finite_json.py",
           "src/governance/evidence_policy.py", "src/governance/anti_hallucination.py",
           "src/governance/retrieval.py", "src/models/llm_model.py", "src/utils/experiment_io.py"]


class QuestionOnlyRetriever:
    """An explicit control: only material included in the question is available."""
    def search(self, question, top_k=2, min_score=1.5):
        return []


def make_governance(config, corpus):
    scope = config.get("evidence_scope", "retrieval")
    if scope not in ("retrieval", "question_only"):
        raise ValueError("Unknown evidence scope")
    retriever = QuestionOnlyRetriever() if scope == "question_only" else LocalRetriever(corpus)
    return EvidencePolicy(retriever, **config["retrieval"])


def generation_tasks(payload, schemas):
    # Drop grading metadata at the generation boundary.
    tasks = [{k: item[k] for k in ("id", "question", "category")} for item in payload["items"]]
    ids = [str(t["id"]) for t in tasks]
    if not tasks or len(set(ids)) != len(ids) or set(ids) != set(schemas):
        raise ValueError("Unique tasks must match the declared output schemas")
    if any(t["category"] != "normal_control" or not isinstance(t["question"], str) or not t["question"].strip() for t in tasks):
        raise ValueError("This experiment accepts nonempty supplied-material control questions only")
    return tasks, {ident: allowed_outputs(schemas[ident]) for ident in ids}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=ROOT / "configs/c_structured_comparison.json")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--retry-errors", action="store_true")
    parser.add_argument("--stop-after", type=int)
    args = parser.parse_args()
    config = json.loads(args.config.read_text(encoding="utf-8"))
    if not config["policies"] or not set(config["policies"]).issubset(POLICIES) or len(config["policies"]) != len(set(config["policies"])) or config["decoders"] != ["free", "json"]:
        raise ValueError("Use distinct known policies and both free/json decoders")
    if config["generation"] != {"max_new_tokens": 192, "do_sample": False}:
        raise ValueError("This comparison fixes greedy generation and a 192-token budget")
    paths = {name: ROOT / config[name] for name in ("controls", "schemas", "corpus")}
    payload = json.loads(paths["controls"].read_text(encoding="utf-8"))
    schemas = json.loads(paths["schemas"].read_text(encoding="utf-8"))["schemas"]
    tasks, outputs = generation_tasks(payload, schemas)
    modes = [(p, d) for p in config["policies"] for d in config["decoders"]]
    planned, mode_info = [], {p + "__" + d: (p, d) for p, d in modes}
    for index, task in enumerate(tasks):
        for policy, decoder in modes[index % len(modes):] + modes[:index % len(modes)]:
            planned.append((str(task["id"]), policy + "__" + decoder))
    model_path = ROOT / config["model_path"]
    contract = {"config": config, "dry_run": args.dry_run, "python": platform.python_version(),
                **{name + "_sha256": sha256_file(path) for name, path in paths.items()},
                "runtime_sha256": {name: sha256_file(ROOT / name) for name in RUNTIME},
                "model_sha256": {} if args.dry_run else {p.name: sha256_file(p) for p in model_path.glob("*") if p.suffix in (".json", ".txt", ".safetensors")}}
    ledger = RunLedger(args.output, contract, planned, args.resume)
    if not args.resume:
        (args.output / "config.json").write_bytes(args.config.read_bytes())
        for name, path in paths.items():
            (args.output / (name + ".json")).write_bytes(path.read_bytes())
        for name in RUNTIME:
            snapshot = args.output / "source_snapshot" / name
            snapshot.parent.mkdir(parents=True, exist_ok=True)
            snapshot.write_bytes((ROOT / name).read_bytes())
    else:
        for name in paths:
            if sha256_file(args.output / (name + ".json")) != contract[name + "_sha256"]:
                raise ValueError("Modified frozen structured experiment input")
        for name, expected in contract["runtime_sha256"].items():
            if sha256_file(args.output / "source_snapshot" / name) != expected:
                raise ValueError("Modified generation source snapshot")
    pending = ledger.pending(args.retry_errors)
    governance = make_governance(config, paths["corpus"])
    by_id = {str(t["id"]): t for t in tasks}
    ledger.manifest.update(status="running", stage=config["stage"])
    ledger.save()
    try:
        model = None
        if pending and not args.dry_run:
            import torch
            import transformers
            from transformers import set_seed
            from src.models.llm_model import LLMModel
            set_seed(config["seed"])
            model = LLMModel(str(model_path), local_files_only=True)
            model.generate("你好", max_new_tokens=8, do_sample=False)
            if torch.cuda.is_available():
                torch.cuda.synchronize()
            ledger.manifest.update(torch=torch.__version__, transformers=transformers.__version__, device=model.device)
        for index, (ident, mode) in enumerate(pending, 1):
            policy, decoder = mode_info[mode]
            task = by_id[ident]
            row = {**task, "mode": mode, "policy": policy, "decoder": decoder, "data_role": "source_bound_control",
                   "evaluation_status": "pending_automated_diagnostic_check", "answer": None,
                   "model_calls": 0, "output_tokens": 0, "input_tokens": 0, "truncated": False,
                   "generation_seconds": 0.0, "constraint_compile_seconds": 0.0,
                   "answer_origin": "dry_run" if args.dry_run else "model"}
            try:
                start = time.perf_counter()
                row.update(governance.prepare(task["question"], policy, task["category"]))
                row["mode"] = mode
                if row["answer_override"] is not None:
                    raise ValueError("Supplied-material controls must use the model, not a program answer")
                row.update(prepare_seconds=time.perf_counter() - start,
                           allowed_outputs=outputs[ident] if decoder == "json" else [],
                           allowed_outputs_sha256=stable_hash(outputs[ident]) if decoder == "json" else None)
                if model is not None:
                    kwargs = dict(config["generation"])
                    if decoder == "json":
                        start = time.perf_counter()
                        chat = model.tokenizer.apply_chat_template([{"role": "user", "content": row["prompt"]}], tokenize=False, add_generation_prompt=True)
                        length = len(model.tokenizer(chat)["input_ids"])
                        eos = model.model.generation_config.eos_token_id
                        grammar = FiniteJsonConstraint(model.tokenizer, outputs[ident], length,
                                                       eos if isinstance(eos, list) else [eos], kwargs["max_new_tokens"])
                        kwargs["prefix_allowed_tokens_fn"] = grammar.allowed_tokens
                        row.update(constraint_compile_seconds=time.perf_counter() - start,
                                   token_paths_sha256=stable_hash(grammar.paths),
                                   longest_allowed_output_tokens=max(map(len, grammar.paths)))
                    set_seed(config["seed"])
                    if torch.cuda.is_available():
                        torch.cuda.synchronize()
                    start = time.perf_counter()
                    row["answer"] = model.generate(row["prompt"], **kwargs)
                    if torch.cuda.is_available():
                        torch.cuda.synchronize()
                    row.update(model.last_generation, model_calls=1, generation_seconds=time.perf_counter() - start)
                    if decoder == "json" and row["answer"] not in outputs[ident]:
                        raise ValueError("Generation failed to complete an allowed JSON object")
                row["status"] = "prepared" if args.dry_run else "ok"
            except Exception as exc:
                row.update(status="error", error=f"{type(exc).__name__}: {exc}")
            ledger.append(row)
            print(f"{index}/{len(pending)} {ident} {mode} {row['status']}", flush=True)
            if args.stop_after and index >= args.stop_after and index < len(pending):
                ledger.manifest["status"] = "interrupted"
                ledger.save()
                return
        ledger.manifest["status"] = "completed_with_errors" if ledger.manifest["counts"]["errors"] else "completed"
        ledger.save()
        if ledger.manifest["counts"]["errors"]:
            raise SystemExit(1)
    except BaseException:
        if ledger.manifest["status"] == "running":
            ledger.manifest["status"] = "interrupted"
            ledger.save()
        raise


if __name__ == "__main__":
    main()
