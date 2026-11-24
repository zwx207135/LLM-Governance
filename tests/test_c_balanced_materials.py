import copy
import json
import unittest
from collections import Counter, defaultdict
from pathlib import Path

from experiments.build_c_balanced_materials import build_payload
from experiments.run_c_structured_comparison import generation_tasks, make_governance

ROOT = Path(__file__).resolve().parents[1]


class BalancedMaterialTests(unittest.TestCase):
    def setUp(self):
        self.specs = json.loads((ROOT / "datasets/controls/c_balanced_material_specs.json").read_text(encoding="utf-8"))
        self.payload, self.schemas = build_payload(self.specs)

    def test_three_verdicts_and_three_basis_choices_are_balanced(self):
        self.assertEqual(Counter(i["expected_fields"]["verdict"] for i in self.payload["items"]),
                         {"supported": 16, "refuted": 16, "not_established": 16})
        self.assertEqual(Counter(i["expected_fields"]["basis"] for i in self.payload["items"]), {"M1": 16, "M2": 16, "none": 16})

    def test_swap_changes_positions_only_and_flips_known_evidence_gold(self):
        pairs = defaultdict(list)
        for item in self.payload["items"]:
            pairs[item["case_pair_id"]].append(item)
        self.assertEqual(len(pairs), 24)
        for pair in pairs.values():
            a, b = sorted(pair, key=lambda r: r["position_variant"])
            self.assertEqual(a["claim"], b["claim"])
            self.assertEqual(a["materials"][0]["text"], b["materials"][1]["text"])
            self.assertEqual(a["materials"][1]["text"], b["materials"][0]["text"])
            self.assertEqual(a["expected_fields"]["verdict"], b["expected_fields"]["verdict"])
            expected = {"M1": "M2", "M2": "M1", "none": "none"}[a["expected_fields"]["basis"]]
            self.assertEqual(b["expected_fields"]["basis"], expected)

    def test_topic_groups_contain_all_six_related_variants(self):
        groups = defaultdict(list)
        for item in self.payload["items"]:
            groups[item["contrast_group"]].append(item)
        self.assertEqual(len(groups), 8)
        self.assertTrue(all(len(group) == 6 for group in groups.values()))

    def test_all_nine_output_combinations_remain_independent_of_gold(self):
        tasks, outputs = generation_tasks(self.payload, self.schemas["schemas"])
        changed = copy.deepcopy(self.payload)
        for item in changed["items"]:
            item["expected_fields"] = {"TEST_ONLY": "wrong_gold"}
        self.assertEqual((tasks, outputs), generation_tasks(changed, self.schemas["schemas"]))
        self.assertTrue(all(len(v) == 9 for v in outputs.values()))

    def test_question_only_scope_cannot_retrieve_external_passages(self):
        config = {"evidence_scope": "question_only", "retrieval": {"top_k": 2, "min_score": 1.5}}
        governance = make_governance(config, ROOT / "does_not_exist.json")
        for policy in ("legacy", "compact"):
            prepared = governance.prepare("太阳是什么？", policy, "normal_control")
            self.assertEqual(prepared["evidence"], [])

    def test_invalid_evidence_scope_cannot_silently_fall_back_to_retrieval(self):
        with self.assertRaises(ValueError):
            make_governance({"evidence_scope": "typo"}, ROOT / "knowledge/corpus_v3.json")

    def test_material_build_is_deterministic(self):
        self.assertEqual(build_payload(self.specs), build_payload(self.specs))
