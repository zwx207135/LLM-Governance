import copy
import json
import unittest

from experiments.prepare_c_pilot_review import FOLDER, validate_rows
from experiments.check_c_pilot_review import check


class PilotReviewTests(unittest.TestCase):
    def setUp(self):
        self.p = json.loads((FOLDER / "draft_payload.json").read_text(encoding="utf-8"))

    def validate(self, rows):
        return validate_rows(self.p["original"], rows, self.p["notes"])

    def test_delivered_workbook_preserves_all_source_text(self):
        self.assertTrue(check()["xlsx_csv_and_evidence_verified"])

    def test_ai_cannot_claim_human_or_adjudication(self):
        for field, value in (("annotator", "C"), ("review_status", "completed"), ("adjudication", "accepted")):
            rows = copy.deepcopy(self.p["draft"])
            rows[0][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                self.validate(rows)

    def test_unknown_entity_cannot_be_given_unproved_truth(self):
        rows = copy.deepcopy(self.p["draft"])
        next(r for r in rows if r["id"] == "26")["core_answer_correct"] = "incorrect"
        with self.assertRaises(ValueError):
            self.validate(rows)

    def test_revised_question_cannot_replace_original(self):
        rows = copy.deepcopy(self.p["draft"])
        next(r for r in rows if r["id"] == "38")["question"] = "开发修订题"
        with self.assertRaises(ValueError):
            self.validate(rows)

    def test_missing_answer_is_not_a_complete_delivery(self):
        with self.assertRaises(ValueError):
            self.validate(self.p["draft"][:-1])

    def test_invalid_refusal_label_is_rejected(self):
        rows = copy.deepcopy(self.p["draft"])
        rows[0]["refusal_type"] = "correct"
        with self.assertRaises(ValueError):
            self.validate(rows)
