import unittest
from pathlib import Path

from experiments.demo_c_governance import validate_items
from src.governance.anti_hallucination import AntiHallucination
from src.governance.evidence_policy import ABSTENTION
from src.governance.retrieval import LocalRetriever
from src.governance.service import GovernanceService

ROOT = Path(__file__).resolve().parents[1]


class ServiceTests(unittest.TestCase):
    def setUp(self):
        self.loads = 0
        self.calls = []
        parent = self

        class Model:
            last_generation = {"input_tokens": 10, "output_tokens": 3, "truncated": False}

            def generate(self, prompt, **kwargs):
                parent.calls.append((prompt, kwargs))
                return "测试模型回答"

        def factory():
            self.loads += 1
            return Model()

        self.retriever = LocalRetriever(ROOT / "knowledge/corpus_v3.json")
        self.service = GovernanceService(self.retriever, factory)

    def test_guard_does_not_load_or_call_model(self):
        row = self.service.answer("中国的首都是哪个城市？", "guarded", "factual")
        self.assertEqual((self.loads, len(self.calls)), (0, 0))
        self.assertEqual((row["answer"], row["answer_origin"], row["output_tokens"]), (ABSTENTION, "policy_abstention", 0))

    def test_prepare_only_never_counts_as_answer(self):
        row = self.service.answer("光速是多少？", "combined", prepare_only=True)
        self.assertEqual((row["status"], row["answer_origin"], row["answer"]), ("prepared", "dry_run", None))
        self.assertEqual(self.loads, 0)

    def test_model_is_loaded_once_and_original_prompt_is_preserved(self):
        for mode in ("baseline", "combined"):
            row = self.service.answer("声音能在真空传播吗？", mode, "factual", 64)
            self.assertEqual(row["prompt"], AntiHallucination(self.retriever).prepare(row["question"], mode, "factual")["prompt"])
            self.assertEqual((row["answer_origin"], row["model_calls"], row["output_tokens"]), ("model", 1, 3))
        self.assertEqual((self.loads, len(self.calls)), (1, 2))
        self.assertEqual(self.calls[0][1], {"max_new_tokens": 64, "do_sample": False})

    def test_unknown_entity_guard_and_math_bypass_remain_distinct(self):
        row = self.service.answer('介绍“王明远”的相对论贡献', "guarded", "general")
        self.assertEqual(row["guard_reason"], "quoted_subject_not_in_evidence")
        math = self.service.answer("求x²=144的全部实数解", "guarded", "math_logic")
        self.assertEqual((math["retrieval_status"], math["answer_origin"]), ("task_bypass", "model"))

    def test_demo_rejects_reference_leakage_duplicate_ids_and_empty_questions(self):
        for items in ([{"id": 1, "question": "Q", "reference": "gold"}],
                      [{"id": 1, "question": "Q"}, {"id": "1", "question": "Q2"}],
                      [{"id": 1, "question": " "}]):
            with self.assertRaises(ValueError):
                validate_items(items)

    def test_invalid_generation_limit_fails_before_model_load(self):
        with self.assertRaises(ValueError):
            self.service.answer("Q", max_new_tokens=0)
        self.assertEqual(self.loads, 0)
