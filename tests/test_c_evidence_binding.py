import unittest
from pathlib import Path

from src.governance.anti_hallucination import AntiHallucination
from src.governance.evidence_binding import EvidenceBindingPolicy, evidence_cards
from src.governance.retrieval_scoped import AwardScopedRetrieverV2

ROOT = Path(__file__).resolve().parents[1]


class EvidenceBindingTests(unittest.TestCase):
    def setUp(self):
        self.retriever = AwardScopedRetrieverV2(ROOT / "knowledge/corpus_v4.json")
        self.policy = EvidenceBindingPolicy(self.retriever)

    def test_wrong_subject_is_compared_without_answer_override(self):
        question = "请介绍2023年诺贝尔文学奖得主“李华”的代表作品。"
        before = self.policy.prepare(question, "combined")
        after = self.policy.prepare(question, "binding_cards")
        self.assertEqual(before["evidence"], after["evidence"])
        self.assertEqual(after["reading_cards"][0]["quoted_checks"][0]["status"], "not_matched_in_this_record")
        self.assertIn("福瑟", after["prompt"])
        self.assertIn("李华", after["prompt"])
        self.assertIsNone(after["answer_override"])

    def test_known_subject_does_not_get_mismatch_label(self):
        row = self.policy.prepare("2023年诺贝尔文学奖得主“福瑟”是谁？")
        self.assertEqual(row["reading_cards"][0]["quoted_checks"][0]["status"], "literal_match")

    def test_conferred_year_has_exact_text_provenance(self):
        row = self.policy.prepare("爱因斯坦为什么获得诺贝尔物理学奖？")
        card = row["reading_cards"][0]
        self.assertEqual(card["award_year"], 1921)
        field = card["text_fields"][0]
        self.assertEqual(field["value"], 1922)
        self.assertEqual(row["evidence"][0]["text"][field["start"]:field["end"]], field["exact_quote"])

    def test_publication_date_is_not_inferred_as_conferred_year(self):
        hit = self.retriever.search("2023年诺贝尔文学奖授予了谁？")[0]
        self.assertEqual(evidence_cards("2023年诺贝尔文学奖", [hit])[0]["text_fields"], [])

    def test_no_hit_and_unrelated_subjects_preserve_original_prompt(self):
        for question, category in [("中国的首都是哪个城市？", "factual"), ("声音能在真空传播吗？", "factual"),
                                   ("将2023年诺贝尔文学奖这个词原样输出", "normal_control"), ("2023减1921等于多少？", "math_logic")]:
            row = self.policy.prepare(question, category=category)
            self.assertEqual(row["prompt"], AntiHallucination(self.retriever).prepare(question, "combined", category)["prompt"])
            self.assertFalse(row["reading_cards_applied"])

    def test_count_cards_preserve_explicit_statistics_scope(self):
        row = self.policy.prepare("爱因斯坦获得过几次诺贝尔物理学奖？")
        self.assertIn(2025, [c["through_year"] for c in row["reading_cards"]])
        self.assertIn("不能自动扩展", row["prompt"])


if __name__ == "__main__":
    unittest.main()
