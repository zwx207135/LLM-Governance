import unittest
from pathlib import Path

from src.governance.retrieval_scoped import AwardScopedRetrieverV2
from src.governance.retrieval_year_alias import AwardYearAliasRetriever

ROOT = Path(__file__).resolve().parents[1]


class YearAliasTests(unittest.TestCase):
    def setUp(self):
        self.retriever = AwardYearAliasRetriever(ROOT / "knowledge/corpus_v4.json")

    def test_year_forms_retrieve_existing_award(self):
        for question in ["1921年度诺贝尔物理学奖实际在哪一年颁发？", "1921 年诺贝尔物理学奖的获奖者是谁？", "诺贝尔物理学奖1921年度的获奖者是谁？"]:
            result = self.retriever.search_with_diagnostics(question)
            self.assertEqual([h["id"] for h in result["hits"]], ["nobel-einstein-1921"])
            self.assertTrue(result["query_expansion"])
            self.assertIn("爱因斯坦", result["query_expansion"]["effective_query"])

    def test_no_cross_year_or_category_fallback(self):
        for question in ["1922年度诺贝尔物理学奖获奖者是谁？", "1921年度诺贝尔文学奖获奖者是谁？", "1921年度诺贝尔奖颁发给谁？"]:
            self.assertEqual(self.retriever.search(question), [])

    def test_existing_hits_and_non_award_queries_are_unchanged(self):
        original = AwardScopedRetrieverV2(ROOT / "knowledge/corpus_v4.json")
        for question in ["2023年诺贝尔物理学奖授予了谁？", "太阳是恒星吗？", "中国的首都是哪个城市？", "爱因斯坦获得过几次诺贝尔物理学奖？"]:
            self.assertEqual(self.retriever.search(question), original.search(question))
            self.assertIsNone(self.retriever.search_with_diagnostics(question)["query_expansion"])


if __name__ == "__main__":
    unittest.main()
