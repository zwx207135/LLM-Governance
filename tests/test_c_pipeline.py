import json
import tempfile
import unittest
from pathlib import Path

from experiments.build_c_knowledge import build, validate_document
from experiments.prepare_c_development import LEAKAGE_GROUPS, prepare
from src.utils.experiment_io import RunLedger, latest_records, read_records

ROOT = Path(__file__).resolve().parents[1]


class LedgerTests(unittest.TestCase):
    def test_resume_skips_success_and_can_retry_errors(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "run"
            plan = [("1", "baseline"), ("1", "combined")]
            ledger = RunLedger(path, {"version": 1}, plan)
            ledger.append({"id": 1, "mode": "baseline", "status": "ok", "answer": "saved"})
            ledger.append({"id": 1, "mode": "combined", "status": "error"})
            resumed = RunLedger(path, {"version": 1}, plan, resume=True)
            self.assertEqual(resumed.pending(), [])
            self.assertEqual(resumed.pending(retry_errors=True), [("1", "combined")])
            resumed.append({"id": 1, "mode": "combined", "status": "ok", "answer": "retry"})
            self.assertEqual(resumed.latest[("1", "combined")]["attempt"], 2)
            self.assertEqual(resumed.manifest["counts"]["ok"], 2)
            self.assertEqual(len(read_records(path / "records.jsonl")), 3)

    def test_changed_contract_is_rejected_before_mutation(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "run"
            RunLedger(path, {"corpus": "old"}, [("1", "baseline")])
            original = (path / "manifest.json").read_bytes()
            with self.assertRaises(ValueError):
                RunLedger(path, {"corpus": "new"}, [("1", "baseline")], resume=True)
            self.assertEqual((path / "manifest.json").read_bytes(), original)

    def test_torn_final_append_is_backed_up_and_recovered(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "run"
            plan = [("1", "baseline"), ("2", "baseline")]
            ledger = RunLedger(path, {}, plan)
            ledger.append({"id": 1, "mode": "baseline", "status": "ok"})
            with ledger.path.open("ab") as stream:
                stream.write(b'{"id":2,"mode":')
            resumed = RunLedger(path, {}, plan, resume=True)
            self.assertEqual(resumed.pending(), [("2", "baseline")])
            self.assertEqual(len(list(path.glob("*.bak"))), 1)

    def test_complete_corrupt_record_is_not_silently_dropped(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "records.jsonl"
            path.write_bytes(b'{"id":1,not-json}\n')
            with self.assertRaises(ValueError):
                read_records(path, repair_tail=True)

    def test_duplicate_attempts_are_rejected(self):
        record = {"id": 1, "mode": "baseline", "status": "ok", "attempt": 1}
        with self.assertRaises(ValueError):
            latest_records([record, record])


class KnowledgeAndUsageTests(unittest.TestCase):
    def test_source_builder_is_deterministic_and_rejects_answer_fields(self):
        base = json.loads((ROOT / "knowledge/corpus.json").read_text(encoding="utf-8"))
        docs = json.loads((ROOT / "knowledge/source_documents.json").read_text(encoding="utf-8"))
        self.assertEqual(build(base, docs), build(base, docs))
        doc = dict(docs["documents"][0], reference="hidden gold answer")
        with self.assertRaises(ValueError):
            validate_document(doc)

    def test_unknown_entities_have_no_truth_reference_in_development(self):
        audit = json.loads((ROOT / "docs/c_work/data_audit.json").read_text(encoding="utf-8"))
        candidates = json.loads((ROOT / "docs/c_work/reviewed_candidate.json").read_text(encoding="utf-8"))
        rows, usage, selected = prepare(audit, candidates)
        by_id = {r["id"]: r for r in rows}
        self.assertIsNone(by_id[28]["reference"])
        self.assertEqual(by_id[28]["data_role"], "uncertainty_probe")
        self.assertIsNotNone(by_id[27]["reference"])
        self.assertEqual(by_id[27]["data_role"], "provisional_reference")
        self.assertFalse(any(r["approved_for_final_test"] for r in rows))
        for group in LEAKAGE_GROUPS:
            self.assertIn(len(set(group).intersection(selected)), (0, len(group)))
        self.assertTrue(all(u["formal_test_status"] == "not_designated" for u in usage))


if __name__ == "__main__":
    unittest.main()
