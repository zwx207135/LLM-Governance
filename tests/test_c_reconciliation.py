import unittest

from src.evaluation.reconciliation import identity, reconcile
from src.evaluation.review_metrics import LABELS, fingerprint, validate_review


class ReconciliationTests(unittest.TestCase):
    def setUp(self):
        self.record = {"id": 101, "mode": "combined", "question": "1+1等于多少？", "answer": "2",
                       "data_role": "provisional_reference", "status": "ok"}
        self.a = {"run": "test_fixture", "id": 101, "mode": "combined", "content_sha256": fingerprint(self.record),
                  "reviewer_id": "A", "reviewer_type": "human", "rationale": "依据算式核查。", "source_ids": ["math:101"],
                  "core_answer": "correct", "factual_error": "absent", "unsupported_claims": "no",
                  "premise_handling": "not_applicable", "refusal": "none", "response_type": "substantive", "evidence_use": "not_applicable"}
        self.b = {**self.a, "reviewer_id": "B", "rationale": "另一位独立复核的测试输入。"}
        self.records = {identity(self.a): self.record}

    def conflict(self):
        b = {**self.b, "factual_error": "present"}
        result = reconcile([self.a, b])
        group = result["review_groups"][0]
        decision = {"resolution_id": group["resolution_id"], "review_group_sha256": group["review_group_sha256"],
                    **{k: self.a[k] for k in LABELS}, "source_ids": "math:101", "rationale": "重查算式后确认结果正确。"}
        return b, result, decision

    def test_ai_only_produces_no_human_result(self):
        result = reconcile([{**self.a, "reviewer_type": "ai_developer"}])
        self.assertEqual(result["report"]["status"], "no_independent_human_reviews")
        self.assertEqual(result["report"]["ai_judgments_excluded"], 1)
        self.assertEqual(result["resolved_records"], [])
        self.assertEqual(result["report"]["tables"], [])
        self.assertTrue(all(v["n"] == 0 for v in result["report"]["agreement_before_adjudication"].values()))

    def test_identical_full_label_sets_count_as_one_consensus_answer(self):
        result = reconcile([self.a, self.b])
        self.assertEqual(result["report"]["consensus_answers"], 1)
        self.assertEqual(result["report"]["human_judgment_records"], 2)
        self.assertEqual(result["report"]["tables"][0]["core_correct_denominator"], 1)
        self.assertEqual(result["resolved_records"][0]["reviewer_ids"], ["A", "B"])
        self.assertNotIn("reviewer_type", result["resolved_records"][0])

    def test_same_core_label_does_not_hide_other_disagreements(self):
        _, result, _ = self.conflict()
        self.assertEqual(result["review_groups"][0]["disagreement_dimensions"], ["factual_error"])
        self.assertEqual(result["report"]["unresolved_conflict_answers"], 1)
        self.assertEqual(result["report"]["tables"], [])
        self.assertEqual(result["report"]["agreement_before_adjudication"]["factual_error"]["agreement_numerator"], 0)

    def test_adjudication_preserves_disagreement_and_single_answer_count(self):
        b, before, decision = self.conflict()
        result = reconcile([self.a, b], [decision], "C", self.records, {"math:101"})
        self.assertEqual(result["report"]["status"], "resolved_reviewed_subset")
        self.assertEqual(result["report"]["adjudicated_answers"], 1)
        self.assertEqual(result["report"]["agreement_before_adjudication"], before["report"]["agreement_before_adjudication"])
        self.assertEqual(result["review_groups"][0]["original_reviews"][1]["factual_error"], "present")
        self.assertEqual(result["report"]["tables"][0]["reviewed"], 1)

    def test_single_human_and_ai_do_not_make_a_pair(self):
        result = reconcile([self.a, {**self.b, "reviewer_type": "ai_developer"}])
        self.assertEqual(result["report"]["single_review_answers"], 1)
        self.assertEqual(result["report"]["resolved_answers"], 0)

    def test_changing_original_rationale_invalidates_existing_decision(self):
        b, _, decision = self.conflict()
        with self.assertRaisesRegex(ValueError, "Original reviews changed"):
            reconcile([{**self.a, "rationale": "修改过的判断理由"}, b], [decision], "C", self.records, {"math:101"})

    def test_duplicate_or_extra_reviewers_are_not_silently_pooled(self):
        for rows in ([self.a, self.a], [self.a, self.b, {**self.a, "reviewer_id": "C"}]):
            with self.assertRaises(ValueError):
                reconcile(rows)

    def test_decision_cannot_turn_unknown_entity_into_a_truth_label(self):
        a = {**self.a, "core_answer": "unverifiable"}
        b = {**self.b, "core_answer": "unverifiable", "refusal": "unclear"}
        pending = reconcile([a, b])["review_groups"][0]
        decision = {"resolution_id": pending["resolution_id"], "review_group_sha256": pending["review_group_sha256"],
                    **{k: self.a[k] for k in LABELS}, "source_ids": ["math:101"], "rationale": "测试拒绝越界裁决。"}
        unknown = {**self.record, "data_role": "uncertainty_probe"}
        with self.assertRaisesRegex(ValueError, "Unestablished entity truth"):
            reconcile([a, b], [decision], "C", {identity(a): unknown}, {"math:101"})

    def test_decision_requires_evidence_and_explicit_identity(self):
        b, _, decision = self.conflict()
        for altered, reviewer in ((decision, " "), ({**decision, "source_ids": []}, "C"),
                                  ({**decision, "rationale": ""}, "C"), ({**decision, "core_answer": ""}, "C")):
            with self.assertRaises(ValueError):
                reconcile([self.a, b], [altered], reviewer, self.records, {"math:101"})

    def test_duplicate_decisions_and_decisions_for_consensus_are_rejected(self):
        b, _, decision = self.conflict()
        for reviews, decisions in (([self.a, b], [decision, decision]), ([self.a, self.b], [decision])):
            with self.assertRaises(ValueError):
                reconcile(reviews, decisions, "C", self.records, {"math:101"})

    def test_unknown_core_is_excluded_but_other_label_agreement_is_retained(self):
        rows = [{**r, "core_answer": "unverifiable"} for r in [self.a, self.b]]
        scores = reconcile(rows)["report"]["agreement_before_adjudication"]
        self.assertEqual(scores["core_answer"]["n"], 0)
        self.assertEqual(scores["factual_error"]["n"], 1)

    def test_bad_attribution_error_outputs_and_scalar_sources_are_rejected(self):
        for review, record in (({**self.a, "reviewer_id": " A"}, self.record),
                               ({**self.a, "source_ids": "math:101"}, self.record),
                               (self.a, {**self.record, "status": "error"})):
            with self.assertRaises(ValueError):
                validate_review(review, record, {"math:101"})
