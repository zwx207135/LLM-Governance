"""Reference-free application interface with lazy generation and explicit output origin."""
import time

from src.governance.anti_hallucination import AntiHallucination, MODES
from src.governance.evidence_policy import EvidencePolicy, POLICIES

STRATEGIES = tuple(MODES) + tuple(POLICIES)


class GovernanceService:
    def __init__(self, retriever, model_factory, synchronize=None, top_k=2, min_score=1.5):
        self.original = AntiHallucination(retriever, top_k, min_score)
        self.candidates = EvidencePolicy(retriever, top_k, min_score)
        self.model_factory = model_factory
        self.model = None
        self.synchronize = synchronize or (lambda: None)

    def prepare(self, question, strategy="combined", category=None):
        if not isinstance(question, str) or not question.strip():
            raise ValueError("Question must be nonempty text")
        if strategy not in STRATEGIES:
            raise ValueError("Unknown strategy")
        if strategy in MODES:
            prepared = self.original.prepare(question, strategy, category)
            prepared.update(answer_override=None, guard_reason=None,
                            evidence_labels={h["id"]: h["id"] for h in prepared["evidence"]})
        else:
            prepared = self.candidates.prepare(question, strategy, category)
        return {**prepared, "question": question, "category": category}

    def answer(self, question, strategy="combined", category=None, max_new_tokens=192, prepare_only=False):
        if not isinstance(max_new_tokens, int) or not 1 <= max_new_tokens <= 2048:
            raise ValueError("max_new_tokens must be between 1 and 2048")
        start = time.perf_counter()
        result = self.prepare(question, strategy, category)
        result.update(prepare_seconds=time.perf_counter() - start, model_calls=0,
                      model_load_seconds=0.0, generation_seconds=0.0, input_tokens=0,
                      output_tokens=0, truncated=False, answer=None)
        if prepare_only:
            result.update(status="prepared", answer_origin="dry_run")
        elif result["answer_override"] is not None:
            result.update(status="ok", answer=result["answer_override"], answer_origin="policy_abstention")
        else:
            if self.model is None:
                start = time.perf_counter()
                self.model = self.model_factory()
                self.synchronize()
                result["model_load_seconds"] = time.perf_counter() - start
            self.synchronize()
            start = time.perf_counter()
            answer = self.model.generate(result["prompt"], max_new_tokens=max_new_tokens, do_sample=False)
            self.synchronize()
            result.update(self.model.last_generation)
            result.update(status="ok", answer=answer, answer_origin="model", model_calls=1,
                          generation_seconds=time.perf_counter() - start)
        return result
