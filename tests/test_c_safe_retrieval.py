import json
import tempfile
import unittest
from pathlib import Path

from src.governance.retrieval import LocalRetriever
from src.governance.retrieval_safe import SafeAnchorRetriever, anchor_matches

ROOT = Path(__file__).resolve().parents[1]


class SafeRetrievalTests(unittest.TestCase):
    def test_bell_nobel_and_both_entities(self):
        self.assertFalse(anchor_matches("贝尔", "诺贝尔奖的历史"))
        self.assertTrue(anchor_matches("贝尔", "贝尔与诺贝尔有什么关系？"))
        self.assertTrue(anchor_matches("电话", "诺贝尔与电话的关系"))

    def test_ascii_boundary(self):
        self.assertFalse(anchor_matches("Watt", "wattage"))
        self.assertFalse(anchor_matches("Sun", "Samsung"))
        self.assertTrue(anchor_matches("Watt", "James Watt发明了什么？"))
        self.assertTrue(anchor_matches("Sun", "the SUN的分类"))

    def test_real_corpus_collision_and_positive_control(self):
        old = LocalRetriever(ROOT / "knowledge/corpus_v3.json")
        new = SafeAnchorRetriever(ROOT / "knowledge/corpus_v3.json")
        question = "爱因斯坦获得过几次诺贝尔物理学奖？"
        self.assertIn("bell-history", [h["id"] for h in old.search(question)])
        result = new.search_with_diagnostics(question)
        self.assertNotIn("bell-history", [h["id"] for h in result["hits"]])
        self.assertIn("bell-history", [h["chunk_id"] for h in result["rejected"]])
        for q in ["贝尔在电话发展中做了什么？", "贝尔与诺贝尔和电话有什么关系？"]:
            self.assertEqual(old.search(q), new.search(q))

    def test_filter_backfills_before_top_k(self):
        corpus = {"version": "test", "sources": [{"id": "s", "url": "https://example.org", "accessed_at": "2026-11-23"}],
                  "chunks": [{"id": "bad", "source_id": "s", "topics": ["贝尔"], "text": "诺贝尔物理学奖"},
                             {"id": "good", "source_id": "s", "topics": ["物理学"], "text": "物理学"}]}
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "corpus.json"
            path.write_text(json.dumps(corpus), encoding="utf-8")
            retriever = SafeAnchorRetriever(path)
            self.assertEqual([h["id"] for h in retriever.search("诺贝尔物理学奖", 1, 0)], ["good"])
            with self.assertRaises(ValueError):
                retriever.search("物理学", 0)


if __name__ == "__main__":
    unittest.main()
