import unittest
from pathlib import Path

from src.governance.evidence_policy import ABSTENTION, EvidencePolicy
from src.governance.retrieval import LocalRetriever

ROOT = Path(__file__).resolve().parents[1]


class PolicyTests(unittest.TestCase):
    def setUp(self):
        self.policy = EvidencePolicy(LocalRetriever(ROOT / "knowledge/corpus_v3.json"))

    def test_quoted_subject_must_have_evidence_not_only_matching_topic(self):
        result = self.policy.prepare('请介绍“王明远”在相对论中的贡献。', "guarded", "fictional_entity")
        self.assertTrue(result["evidence"])
        self.assertEqual(result["guard_reason"], "quoted_subject_not_in_evidence")
        self.assertEqual(result["answer_override"], ABSTENTION)

    def test_guard_can_also_abstain_on_a_real_answerable_question(self):
        result = self.policy.prepare("中国的首都是哪个城市？", "guarded", "factual")
        self.assertEqual(result["guard_reason"], "no_retrieved_evidence")
        self.assertEqual(result["answer_override"], ABSTENTION)

    def test_local_tasks_do_not_require_external_knowledge(self):
        for category in ("math_logic", "normal_control"):
            result = self.policy.prepare("把8、3、5从小到大排列", "guarded", category)
            self.assertIsNone(result["answer_override"])
            self.assertEqual(result["retrieval_status"], "task_bypass")

    def test_legacy_prompt_is_preserved(self):
        result = self.policy.prepare("太阳是恒星吗？", "legacy", "factual")
        expected = self.policy.legacy.prepare("太阳是恒星吗？", "combined", "factual")
        self.assertEqual(result["prompt"], expected["prompt"])

    def test_compact_keeps_sources_in_log_without_long_urls_in_prompt(self):
        result = self.policy.prepare("真空光速是多少？", "compact", "factual")
        self.assertTrue(result["evidence"])
        self.assertTrue(result["evidence_labels"])
        self.assertNotIn("https://", result["prompt"])
        self.assertTrue(result["evidence"][0]["source"]["url"].startswith("https://"))


if __name__ == "__main__":
    unittest.main()
