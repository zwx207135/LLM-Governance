import unittest
from pathlib import Path

from src.governance.subject_focus import SubjectFocusPolicy
from src.governance.retrieval_year_alias import AwardYearAliasRetriever

ROOT = Path(__file__).resolve().parents[1]


class SubjectFocusTests(unittest.TestCase):
    def setUp(self):
        self.policy = SubjectFocusPolicy(AwardYearAliasRetriever(ROOT / "knowledge/corpus_v4.json"))

    def test_changes_only_prompt_for_mismatched_subject(self):
        q = "2023年诺贝尔文学奖得主“李华”的代表作是什么？"
        before = self.policy.prepare(q, "combined")
        after = self.policy.prepare(q, "subject_focus")
        self.assertEqual(before["evidence"], after["evidence"])
        self.assertTrue(after["subject_focus_applied"])
        self.assertIsNone(after["answer_override"])
        self.assertIn(q, after["prompt"])

    def test_known_subject_no_hit_and_math_keep_original_prompt(self):
        for q, category in [("2023年诺贝尔文学奖得主“福瑟”的获奖理由是什么？", "factual"),
                             ("“未知产品”多少钱？", "fictional_entity"), ("2023减1921等于多少？", "math_logic")]:
            a = self.policy.prepare(q, "combined", category)
            b = self.policy.prepare(q, "subject_focus", category)
            self.assertEqual(a["prompt"], b["prompt"])
            self.assertFalse(b["subject_focus_applied"])


if __name__ == "__main__":
    unittest.main()
