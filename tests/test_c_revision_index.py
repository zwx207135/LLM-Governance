import copy
import json
import unittest
from pathlib import Path

from experiments.build_c_revision_index import assemble, load_payload, INPUTS

ROOT = Path(__file__).resolve().parents[1]


class RevisionIndexTests(unittest.TestCase):
    def test_actual_counts_distinguish_questions_and_fields(self):
        result = load_payload()
        self.assertEqual(result["summary"]["proposal_entries"], 30)
        self.assertEqual(result["summary"]["distinct_original_items"], 28)
        self.assertEqual(result["summary"]["bounded_alternatives"], 5)
        self.assertEqual(result["summary"]["approved_replacements"], 0)

    def test_conflicting_candidates_are_retained_and_not_selected(self):
        v = [json.loads((ROOT / p).read_text(encoding="utf-8")) for p in INPUTS]
        second = copy.deepcopy(v[2][0]); second["after"] += "待核验补充。"
        result = assemble(v[0], v[1], [("one", v[2]), ("two", [second])], [v[4], v[6]], v[7])
        self.assertEqual(result["summary"]["conflicting_groups"], 1)
        self.assertIsNone(result["selected_replacement"])

    def test_incorrect_original_before_value_is_rejected(self):
        v = [json.loads((ROOT / p).read_text(encoding="utf-8")) for p in INPUTS]
        v[2][0]["before"] = "changed"
        with self.assertRaises(ValueError):
            assemble(v[0], v[1], [("bad", v[2])], [v[4], v[6]], v[7])


if __name__ == "__main__":
    unittest.main()
