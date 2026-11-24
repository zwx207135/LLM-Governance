import unittest
from pathlib import Path

from src.governance.retrieval_scoped import AwardScopedRetriever, AwardScopedRetrieverV2
from src.governance.retrieval_safe import SafeAnchorRetriever

ROOT = Path(__file__).resolve().parents[1]


class ScopedRetrievalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.path = ROOT / "knowledge/corpus_v4.json"
        cls.retriever = AwardScopedRetriever(cls.path)

    def test_award_year_and_category(self):
        for year in (2022, 2023):
            hits = self.retriever.search(f"{year}年诺贝尔物理学奖授予了谁？")
            self.assertEqual([h["id"] for h in hits], [f"nobel-physics-{year}"])
        hits = self.retriever.search("2023年诺贝尔文学奖授予了谁？")
        self.assertEqual([h["id"] for h in hits], ["nobel-literature-2023"])

    def test_uncovered_year_does_not_borrow_another_year(self):
        self.assertEqual(self.retriever.search("2020年诺贝尔物理学奖授予了谁？"), [])

    def test_count_retrieves_individual_and_statistics(self):
        result = self.retriever.search_with_diagnostics("爱因斯坦获得过几次诺贝尔物理学奖？")
        self.assertEqual([h["id"] for h in result["hits"]], ["nobel-einstein-1921", "nobel-physics-repeat-through-2025"])
        self.assertTrue(result["selection_events"])

    def test_quoted_unknown_subject_does_not_borrow_named_records(self):
        self.assertEqual(self.retriever.search("诺贝尔物理学奖得主“陈晓东”是因为什么研究获得该奖项的？"), [])

    def test_non_award_queries_preserve_safe_retrieval(self):
        safe = SafeAnchorRetriever(self.path)
        for question in ["声音能在真空中传播吗？", "既然牛顿是相对论的提出者，那么请介绍他的理论。", "中国的首都是哪个城市？"]:
            self.assertEqual(self.retriever.search(question), safe.search(question))

    def test_multi_year_comparison_keeps_both(self):
        hits = self.retriever.search("比较2022年与2023年诺贝尔物理学奖的研究领域", top_k=10)
        self.assertTrue({"nobel-physics-2022", "nobel-physics-2023"}.issubset({h["id"] for h in hits}))

    def test_v2_keeps_annual_list_to_challenge_wrong_subject(self):
        retriever = AwardScopedRetrieverV2(self.path)
        for question, expected in [("请介绍2023年诺贝尔文学奖得主“李华”的代表作品。", "nobel-literature-2023"),
                                   ("爱因斯坦获得2023年诺贝尔物理学奖的原因是什么？", "nobel-physics-2023")]:
            self.assertEqual([h["id"] for h in retriever.search(question)], [expected])

    def test_v2_award_reason_does_not_borrow_scientific_history(self):
        retriever = AwardScopedRetrieverV2(self.path)
        self.assertEqual([h["id"] for h in retriever.search("爱因斯坦为什么获得诺贝尔物理学奖？")], ["nobel-einstein-1921"])
        self.assertEqual(retriever.search("诺贝尔物理学奖得主“陈晓东”是因为什么研究获奖？"), [])


if __name__ == "__main__":
    unittest.main()
