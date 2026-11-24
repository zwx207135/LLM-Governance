import copy
import json
import unittest
from pathlib import Path

from experiments.check_c_source_bound import check_answer, score_records
from experiments.report_c_source_followup import validate_followup

ROOT = Path(__file__).resolve().parents[1]


class SourceFollowupTests(unittest.TestCase):
    def setUp(self):
        self.payload = json.loads((ROOT / "docs/c_work/source_followup_v1.json").read_text(encoding="utf-8"))
        self.audit = json.loads((ROOT / "docs/c_work/data_audit.json").read_text(encoding="utf-8"))

    def test_all_original_pending_items_are_accounted_for_without_verifying_core_truth(self):
        self.assertEqual(validate_followup(self.payload, self.audit), {"reference_issue": 4, "context_only": 8, "pending_source_review": 5})

    def test_missing_or_duplicate_pending_ids_are_rejected(self):
        for reviews in (self.payload["reviews"][:-1], self.payload["reviews"] + [self.payload["reviews"][0]]):
            with self.assertRaises(ValueError):
                validate_followup({**self.payload, "reviews": reviews}, self.audit)

    def test_context_cannot_be_silently_promoted_to_truth_or_human_approval(self):
        changed = copy.deepcopy(self.payload)
        changed["reviews"][0]["disposition"] = "supported_core"
        with self.assertRaises(ValueError):
            validate_followup(changed, self.audit)
        with self.assertRaises(ValueError):
            validate_followup({**self.payload, "independent_human_reviews_completed": 1}, self.audit)

    def test_positive_finding_requires_registered_sources_and_proposal(self):
        for field, value in (("source_ids", []), ("source_ids", ["invented"]), ("proposed_reference", "")):
            changed = copy.deepcopy(self.payload)
            changed["reviews"][0][field] = value
            with self.assertRaises(ValueError):
                validate_followup(changed, self.audit)


class SourceBoundCheckerTests(unittest.TestCase):
    def setUp(self):
        self.expected = {"namesake_documented": True, "nobel_identity": "not_established"}
        self.good = json.dumps(self.expected)

    def test_code_fences_preserve_content_but_fail_strict_task(self):
        strict = check_answer(self.good, self.expected)
        wrapped = check_answer("```json\n" + self.good + "\n```", self.expected)
        self.assertTrue(strict["strict_task_passed"])
        self.assertTrue(wrapped["content_fields_passed"])
        self.assertFalse(wrapped["strict_task_passed"])

    def test_numeric_one_is_not_boolean_true(self):
        result = check_answer('{"namesake_documented":1,"nobel_identity":"not_established"}', self.expected)
        self.assertFalse(result["content_fields_passed"])

    def test_duplicate_keys_extra_text_and_nonfinite_values_are_not_accepted(self):
        for text in ('{"namesake_documented":false,"namesake_documented":true,"nobel_identity":"not_established"}',
                     "正确答案：" + self.good, self.good + "这是解释", '{"value":NaN}'):
            self.assertFalse(check_answer(text, self.expected)["content_fields_passed"])

    def test_unknown_award_status_is_not_a_false_or_true_award_claim(self):
        for value in ("supported", "refuted"):
            self.assertFalse(check_answer(json.dumps({**self.expected, "nobel_identity": value}), self.expected)["content_fields_passed"])

    def test_unexpected_fields_fail_the_task(self):
        result = check_answer(json.dumps({**self.expected, "year": 2026}), self.expected)
        self.assertFalse(result["content_fields_passed"])
        self.assertTrue(result["required_field_values_passed"])

    def test_changed_question_and_prepared_rows_cannot_reuse_diagnostic_gold(self):
        item = {"id": "B01", "question": "Q", "expected_fields": self.expected}
        row = {"id": "B01", "question": "different", "category": "normal_control", "mode": "legacy", "status": "ok", "answer": self.good}
        with self.assertRaises(ValueError):
            score_records([row], [item])
        with self.assertRaises(ValueError):
            score_records([{**row, "question": "Q", "status": "prepared"}], [item])
