import csv
import tempfile
import unittest
from pathlib import Path

from experiments.report_c_suite import screen, summarize, write_reviews
from experiments.check_c_controls import check


class ReviewReportTests(unittest.TestCase):
    def test_closed_format_check_rejects_answer_embedded_in_explanation(self):
        self.assertTrue(check("N15", '{"name":"小林","task":"检索"}'))
        self.assertFalse(check("N15", '答案是{"name":"小林","task":"检索"}'))
        self.assertFalse(check("N15", '{"name":"小林","task":"检索","extra":"invented"}'))
        self.assertTrue(check("N10", "3、5、8、11"))
        self.assertFalse(check("N10", "3、5、8、11、12"))

    def sample(self):
        return {"id": 1, "mode": "baseline", "category": "factual", "data_role": "provisional_reference",
                "question": "问题", "answer": "原始回答", "status": "ok", "generation_seconds": 1.0,
                "prepare_seconds": .01, "output_tokens": 10, "truncated": False,
                "retrieval_status": "disabled", "evidence": []}

    def test_regeneration_retains_annotations_for_same_content(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "review.csv"
            row = self.sample()
            write_reviews(path, [row])
            with path.open(encoding="utf-8-sig", newline="") as stream:
                reader = csv.DictReader(stream)
                fields, old = reader.fieldnames, list(reader)
            old[0].update(reviewer="D", rationale="Checked complete answer", core_correct="unknown")
            with path.open("w", encoding="utf-8-sig", newline="") as stream:
                writer = csv.DictWriter(stream, fieldnames=fields)
                writer.writeheader()
                writer.writerows(old)
            write_reviews(path, [row])
            with path.open(encoding="utf-8-sig", newline="") as stream:
                actual = next(csv.DictReader(stream))
            self.assertEqual(actual["rationale"], "Checked complete answer")
            self.assertEqual(actual["reviewer"], "D")

    def test_changed_answer_does_not_inherit_old_score(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "review.csv"
            row = self.sample()
            write_reviews(path, [row])
            with path.open(encoding="utf-8-sig", newline="") as stream:
                reader = csv.DictReader(stream)
                fields, old = reader.fieldnames, list(reader)
            old[0].update(reviewer="D", core_correct="yes")
            with path.open("w", encoding="utf-8-sig", newline="") as stream:
                writer = csv.DictWriter(stream, fieldnames=fields)
                writer.writeheader()
                writer.writerows(old)
            write_reviews(path, [{**row, "answer": "不同的回答"}])
            with path.open(encoding="utf-8-sig", newline="") as stream:
                actual = next(csv.DictReader(stream))
            self.assertEqual(actual["core_correct"], "")
            self.assertEqual(len(list(path.parent.glob("review.previous-*.csv"))), 1)

    def test_screening_signal_does_not_create_accuracy(self):
        row = {**self.sample(), "answer": "我不确定", "data_role": "normal_control"}
        self.assertIn("possible_over_refusal", screen(row))
        summary = summarize([row], {"modes": ["baseline"], "development_ids": [1]})
        self.assertIsNone(summary["accuracy"])
        self.assertIsNone(summary["hallucination_rate"])

    def test_pairing_uses_same_sample_not_unpaired_means(self):
        first = self.sample()
        second = {**first, "mode": "combined", "generation_seconds": 1.5}
        unpaired = {**second, "id": 2, "generation_seconds": 50}
        summary = summarize([first, second, unpaired], {"modes": ["baseline", "combined"], "development_ids": [1, 2]})
        combined = summary["modes"][1]
        self.assertEqual(combined["paired_baseline_n"], 1)
        self.assertEqual(combined["paired_mean_generation_delta_seconds"], .5)


if __name__ == "__main__":
    unittest.main()
