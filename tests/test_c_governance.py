import hashlib
import io
import json
import csv
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from experiments.audit_hallucination import audit, load_registry, main as audit_main
from src.governance.anti_hallucination import AntiHallucination
from src.governance.retrieval import LocalRetriever

ROOT = Path(__file__).resolve().parents[1]


class GovernanceTests(unittest.TestCase):
    def setUp(self):
        self.retriever = LocalRetriever(ROOT / "knowledge/corpus.json")
        self.gov = AntiHallucination(self.retriever)

    def test_chinese_evidence_has_provenance(self):
        hit = self.retriever.search("地球唯一的天然卫星是什么？")[0]
        self.assertEqual(hit["id"], "moon-01")
        self.assertTrue(hit["source"]["url"].startswith("https://"))
        self.assertEqual(hit["source"]["accessed_at"], "2026-11-22")

    def test_unknown_entity_is_not_asserted_nonexistent(self):
        result = self.gov.prepare("请介绍虚构的紫色独角兽研究院", "combined")
        self.assertEqual(result["retrieval_status"], "no_hit")
        self.assertEqual(result["evidence"], [])
        self.assertIn("不能证明", result["prompt"])

    def test_math_bypasses_irrelevant_retrieval(self):
        result = self.gov.prepare("地球有8颗卫星，再减去3颗是多少？", "combined", "math_logic")
        self.assertEqual(result["retrieval_status"], "math_bypass")
        self.assertEqual(result["evidence"], [])

    def test_common_words_do_not_admit_off_topic_documents(self):
        self.assertEqual(self.retriever.search("请介绍著名物理学家王明远在相对论研究领域的主要贡献"), [])
        hits = self.retriever.search("世界上面积最大的海洋是哪个？")
        self.assertEqual([h["id"] for h in hits], ["ocean-01"])

    def test_ablations(self):
        q = "太阳是什么？"
        self.assertEqual(self.gov.prepare(q, "baseline")["prompt"], q)
        self.assertEqual(self.gov.prepare(q, "constraint")["retrieval_status"], "disabled")
        self.assertNotIn("回答规则", self.gov.prepare(q, "retrieval")["prompt"])
        self.assertIn("回答规则", self.gov.prepare(q, "combined")["prompt"])

    def test_no_benchmark_fields_in_corpus(self):
        corpus = json.loads((ROOT / "knowledge/corpus.json").read_text(encoding="utf-8"))
        for chunk in corpus["chunks"]:
            self.assertFalse({"question", "reference", "reference_source", "note"}.intersection(chunk))
        self.assertEqual(self.retriever.sha256, hashlib.sha256((ROOT / "knowledge/corpus.json").read_bytes()).hexdigest())

    def test_invalid_provenance_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "bad.json"
            path.write_text(json.dumps({"version": "test", "sources": [{"id": "x"}],
                                        "chunks": [{"id": "c", "source_id": "x", "text": "test"}]}))
            with self.assertRaises(ValueError):
                LocalRetriever(path)

    def test_audit_preserves_original_and_flags_bad_reference(self):
        data = json.loads((ROOT / "datasets/hallucination/test_set.json").read_text(encoding="utf-8"))
        before = json.dumps(data)
        rows = {x["id"]: x for x in audit(data)}
        self.assertEqual(len(rows), 125)
        self.assertEqual(json.dumps(data), before)
        self.assertEqual(rows[111]["reference"], "12")
        self.assertEqual(rows[111]["proposal"]["reference"], "12和-12")
        self.assertEqual(rows[28]["review_status"], "pending_source_review")
        self.assertFalse(any(x["approved_for_final_test"] for x in rows.values()))

    def test_repeatable_ranking_and_invalid_mode(self):
        self.assertEqual(self.retriever.search("太阳系最大的行星"), self.retriever.search("太阳系最大的行星"))
        with self.assertRaises(ValueError):
            self.gov.prepare("问题", "unknown")

    def test_revision_does_not_mean_evidence_is_complete(self):
        data = json.loads((ROOT / "datasets/hallucination/test_set.json").read_text(encoding="utf-8"))
        rows = {r["id"]: r for r in audit(data)}
        self.assertEqual(rows[26]["revision_status"], "proposed")
        self.assertEqual(rows[26]["source_verification_status"], "limited_scope")
        self.assertEqual(rows[63]["source_verification_status"], "reference_issue")
        self.assertEqual(rows[59]["source_verification_status"], "supported_core")
        self.assertFalse(any(r["approved_for_final_test"] for r in rows.values()))

    def test_dates_are_proposed_without_editing_original_questions(self):
        data = json.loads((ROOT / "datasets/hallucination/test_set.json").read_text(encoding="utf-8"))
        rows = {r["id"]: r for r in audit(data)}
        self.assertEqual(rows[59]["question"], "现任联合国秘书长是谁？")
        self.assertIn("2026-11-22", rows[59]["proposal"]["question"])
        self.assertEqual(rows[51]["event_year"], 2022)
        self.assertNotIn("needs_as_of_or_event_date", rows[51]["flags"])

    def test_invalid_source_registry_is_rejected(self):
        registry = json.loads((ROOT / "docs/c_work/source_registry.json").read_text(encoding="utf-8-sig"))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "registry.json"
            registry["reviews"][0]["source_ids"] = ["missing-source"]
            path.write_text(json.dumps(registry), encoding="utf-8")
            with self.assertRaises(ValueError):
                load_registry(path)

    def test_regeneration_preserves_human_annotations_and_original(self):
        original = (ROOT / "datasets/hallucination/test_set.json").read_bytes()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "datasets/hallucination/test_set.json"
            target.parent.mkdir(parents=True)
            target.write_bytes(original)
            output = root / "docs/c_work"
            output.mkdir(parents=True)
            with (output / "data_review.csv").open("w", encoding="utf-8-sig", newline="") as stream:
                writer = csv.DictWriter(stream, fieldnames=["id", "reviewer", "second_reviewer", "human_decision", "human_notes"])
                writer.writeheader()
                writer.writerow({"id": 1, "reviewer": "Reviewer A", "second_reviewer": "Reviewer B",
                                 "human_decision": "needs_discussion", "human_notes": "Keep my independent review"})
            with patch("experiments.audit_hallucination.ROOT", root), patch("sys.stdout", new_callable=io.StringIO):
                audit_main()
            with (output / "data_review.csv").open(encoding="utf-8-sig", newline="") as stream:
                first = next(csv.DictReader(stream))
            self.assertEqual(first["human_notes"], "Keep my independent review")
            self.assertEqual(first["second_reviewer"], "Reviewer B")
            self.assertEqual(target.read_bytes(), original)
            candidate = json.loads((output / "reviewed_candidate.json").read_text(encoding="utf-8"))
            self.assertEqual(candidate["stage"], "proposal_only_not_frozen_test")
            self.assertFalse(any(r["approved_for_final_test"] for r in candidate["items"]))


if __name__ == "__main__":
    unittest.main()
