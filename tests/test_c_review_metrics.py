import unittest

from src.evaluation.review_metrics import agreement, fingerprint, summarize, validate_review


class ReviewMetricsTests(unittest.TestCase):
    def fixture(self):
        record = {"id": 1, "mode": "combined", "question": "问题", "answer": "回答", "data_role": "provisional_reference"}
        review = {"run": "run1", "id": 1, "mode": "combined", "content_sha256": fingerprint(record),
                  "reviewer_id": "developer", "reviewer_type": "ai_developer", "rationale": "依据来源核查完整回答。",
                  "source_ids": ["source"], "core_answer": "correct", "factual_error": "absent",
                  "unsupported_claims": "no", "premise_handling": "not_applicable", "refusal": "none",
                  "response_type": "substantive", "evidence_use": "supported"}
        return record, review

    def test_ai_reviews_do_not_create_human_metrics_or_agreement(self):
        _, review = self.fixture()
        result = summarize([review])
        self.assertEqual(result["status"], "no_independent_human_reviews")
        self.assertEqual(result["tables"], [])
        self.assertIsNone(result["human_agreement"]["kappa"])

    def test_unknown_entity_cannot_be_scored_as_correct_or_false(self):
        record, review = self.fixture()
        record["data_role"] = "uncertainty_probe"
        with self.assertRaises(ValueError):
            validate_review(review, record, {"source"})

    def test_changed_answer_hash_invalidates_review(self):
        record, review = self.fixture()
        record["answer"] = "changed"
        with self.assertRaises(ValueError):
            validate_review(review, record, {"source"})

    def test_same_reviewer_is_not_two_independent_reviewers(self):
        _, review = self.fixture()
        a = {**review, "reviewer_type": "human", "reviewer_id": "A"}
        self.assertEqual(agreement([a, a])["status"], "unavailable")
        with self.assertRaises(ValueError):
            summarize([a, a])

    def test_disagreements_require_adjudication_not_duplicate_counts(self):
        _, review = self.fixture()
        a = {**review, "reviewer_type": "human", "reviewer_id": "A"}
        b = {**a, "reviewer_id": "B", "core_answer": "incorrect"}
        result = summarize([a, b])
        self.assertEqual(result["status"], "adjudication_required")
        self.assertEqual(result["tables"], [])
        self.assertEqual(result["human_agreement"]["n"], 1)

    def test_unverifiable_facts_are_separate_from_false_facts(self):
        _, review = self.fixture()
        unknown = {**review, "id": 2, "core_answer": "unverifiable", "factual_error": "unverifiable"}
        result = summarize([review, unknown], include_ai=True)["tables"][0]
        self.assertEqual(result["core_correct_denominator"], 1)
        self.assertEqual(result["factual_error_denominator"], 1)
        self.assertEqual(result["factual_unverifiable_or_na"], 1)


if __name__ == "__main__":
    unittest.main()
