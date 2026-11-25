import unittest

from experiments.import_c_annotations import import_rows
from src.evaluation.review_metrics import agreement, fingerprint


class AnnotationImportTests(unittest.TestCase):
    def test_empty_template_cannot_be_counted_as_human_review(self):
        with self.assertRaises(ValueError):
            import_rows([{"review_id": "R1"}], {}, "D", "human", {}, set())

    def test_incomplete_annotation_is_rejected(self):
        record = {"id": 1, "mode": "a", "question": "Q", "answer": "A", "data_role": "provisional_reference"}
        mapping = {"R1": {"run": "r", "id": 1, "mode": "a", "content_sha256": fingerprint(record)}}
        with self.assertRaises(ValueError):
            import_rows([{"review_id": "R1", "core_answer": "correct"}], mapping, "D", "human", {("r", "1", "a"): record}, set())

    def test_different_reviewer_pairs_are_not_pooled_into_one_kappa(self):
        base = {"run": "r", "mode": "a", "content_sha256": "hash", "reviewer_type": "human"}
        rows = [{**base, "id": 1, "reviewer_id": "A", "core_answer": "correct"},
                {**base, "id": 1, "reviewer_id": "B", "core_answer": "correct"},
                {**base, "id": 2, "reviewer_id": "C", "core_answer": "correct"},
                {**base, "id": 2, "reviewer_id": "D", "core_answer": "incorrect"}]
        result = agreement(rows)
        self.assertEqual(result["status"], "available_by_reviewer_pair")
        self.assertIsNone(result["kappa"])
        self.assertEqual(len(result["pairs"]), 2)


if __name__ == "__main__":
    unittest.main()
