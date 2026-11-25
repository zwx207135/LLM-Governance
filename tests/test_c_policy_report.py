import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from experiments.report_c_policy_comparison import eligible_controls, load_comparison

ROOT = Path(__file__).resolve().parents[1]


class PolicyReportTests(unittest.TestCase):
    def test_another_run_gets_its_own_report_without_inheriting_case_judgments(self):
        original = ROOT / "docs/c_work/runs/policy_comparison_v1"
        with tempfile.TemporaryDirectory() as directory:
            run = Path(directory)
            for name in ("manifest.json", "dataset.json", "controls.json", "corpus.json", "records.jsonl"):
                shutil.copy(original / name, run)
            subprocess.run([sys.executable, "-m", "experiments.report_c_policy_comparison", str(run)],
                           cwd=ROOT, check=True, capture_output=True)
            report = (run / "report.md").read_text(encoding="utf-8")
            self.assertIn("未关联经哈希核验的事实评分", report)
            self.assertNotIn("单一AI开发者的12例复核", report)
            self.assertNotIn("还编造了10万元售价", report)
            self.assertEqual(json.loads((run / "summary.json").read_text(encoding="utf-8"))["records"], 120)

    def test_reusing_normal_task_id_does_not_reuse_its_grader(self):
        canonical = {"items": [{"id": "N07", "question": "提取甲"}]}
        frozen = {"items": [{"id": "N07", "question": "提取乙"}]}
        row = {"id": "N07", "question": "提取乙", "category": "normal_control"}
        self.assertEqual(eligible_controls([row], frozen, canonical), [])
        row["question"] = "提取甲"
        self.assertEqual(eligible_controls([row], frozen, canonical), [])
        self.assertEqual(eligible_controls([row], canonical, canonical), [row])

    def test_changed_snapshot_is_rejected_before_report_writes(self):
        original = ROOT / "docs/c_work/runs/policy_comparison_v1"
        with tempfile.TemporaryDirectory() as directory:
            run = Path(directory)
            shutil.copy(original / "manifest.json", run)
            (run / "dataset.json").write_text("{}", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Modified dataset snapshot"):
                load_comparison(run)

    def test_complete_manifest_with_error_record_is_rejected(self):
        original = ROOT / "docs/c_work/runs/policy_comparison_v1"
        with tempfile.TemporaryDirectory() as directory:
            run = Path(directory)
            for name in ("manifest.json", "dataset.json", "controls.json", "corpus.json", "records.jsonl"):
                shutil.copy(original / name, run)
            records = [json.loads(line) for line in (run / "records.jsonl").read_text(encoding="utf-8").splitlines()]
            records[0]["status"] = "error"
            (run / "records.jsonl").write_text("\n".join(json.dumps(r) for r in records) + "\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "unsuccessful"):
                load_comparison(run)
