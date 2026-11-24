import copy
import json
import unittest
from pathlib import Path

from experiments.build_c_pending_repairs import validate

ROOT = Path(__file__).resolve().parents[1]


class PendingRepairsTests(unittest.TestCase):
    def setUp(self):
        self.payload = json.loads((ROOT / "docs/c_work/source_followup_pending_v2.json").read_text(encoding="utf-8"))
        self.original = json.loads((ROOT / "datasets/hallucination/test_set.json").read_text(encoding="utf-8"))
        self.prior = json.loads((ROOT / "docs/c_work/source_followup_v1.json").read_text(encoding="utf-8"))

    def check(self):
        return validate(self.payload, self.original, self.prior)

    def test_valid_followup_covers_pending_without_mutating_original(self):
        before = copy.deepcopy(self.original)
        self.check()
        self.assertEqual(self.original, before)
        self.assertEqual({r["id"] for r in self.payload["reviews"]}, {33, 34, 37, 41, 42})

    def test_context_cannot_silently_become_verified_truth(self):
        self.payload["reviews"][0]["target_claim_status"] = "verified"
        with self.assertRaises(ValueError): self.check()

    def test_developer_proposals_cannot_be_autoapproved(self):
        self.payload["reviews"][0]["approved_for_final_test"] = True
        with self.assertRaises(ValueError): self.check()

    def test_changed_task_needs_separate_question_identity(self):
        row = self.payload["reviews"][0]
        row["candidate_question"] = next(x["question"] for x in self.original["items"] if x["id"] == row["id"])
        with self.assertRaises(ValueError): self.check()

    def test_evidence_must_have_registered_source_and_scope(self):
        self.payload["sources"][0]["does_not_support"] = ""
        with self.assertRaises(ValueError): self.check()

    def test_missing_pending_case_is_rejected(self):
        self.payload["reviews"].pop()
        with self.assertRaises(ValueError): self.check()


if __name__ == "__main__":
    unittest.main()
