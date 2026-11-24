import json
import unittest
from pathlib import Path

from experiments.build_c_balanced_materials import build_payload
from experiments.build_c_material_label_followup import translate_payload
from experiments.report_c_balanced_materials import aggregate, prediction, validate_design

ROOT = Path(__file__).resolve().parents[1]


class MaterialMetricTests(unittest.TestCase):
    def case(self, number, variant, expected="not_established", verdict="not_established", basis="none"):
        return {"id": str(number) + variant, "mode": "test", "policy": "test", "decoder": "free",
                "contrast_group": "G", "case_pair_id": str(number), "position_variant": variant,
                "expected_verdict": expected, "predicted_verdict": verdict,
                "predicted_basis": basis, "schema_conformant": True, "strict_task_passed": expected == verdict,
                "verdict_correct": expected == verdict, "basis_correct": basis == "none" and expected == "not_established",
                "joint_correct": expected == verdict and basis == "none" and expected == "not_established"}

    def test_constant_unknown_can_be_stable_without_being_correct(self):
        rows = [self.case(i, v, expected=label) for i, label in enumerate(("supported", "refuted", "not_established")) for v in ("base", "swapped")]
        metric = aggregate(rows)[0][0]
        self.assertEqual(metric["verdict_unchanged_pairs"], 3)
        self.assertEqual(metric["verdict_correct"], 2)
        self.assertEqual(metric["both_joint_correct_pairs"], 1)
        self.assertEqual(metric["known_basis_tracks_swap_pairs"], 0)

    def test_evidence_equivariance_does_not_imply_correct_labels(self):
        a = self.case(1, "base", "refuted", "supported", "M1")
        b = self.case(1, "swapped", "refuted", "supported", "M2")
        metric = aggregate([a, b])[0][0]
        self.assertEqual(metric["known_basis_tracks_swap_pairs"], 1)
        self.assertEqual(metric["both_joint_correct_pairs"], 0)

    def test_no_unpaired_or_duplicate_position_comparison(self):
        for rows in ([self.case(1, "base")], [self.case(1, "base"), self.case(1, "base")]):
            with self.assertRaises(ValueError):
                aggregate(rows)

    def test_invalid_json_and_unquoted_enum_are_not_repaired(self):
        for text in ('{"verdict":supported,"basis":"M1"}', '说明：{"verdict":"supported","basis":"M1"}'):
            self.assertEqual(prediction(text)["predicted_verdict"], "invalid")

    def test_complete_fenced_object_is_separate_from_bare_format(self):
        parsed = prediction('```json\n{"verdict":"refuted","basis":"M2"}\n```')
        self.assertEqual(parsed["predicted_verdict"], "refuted")
        self.assertEqual(parsed["parse_status"], "fenced_json")

    def test_chinese_mapping_does_not_guess_undeclared_english_labels(self):
        mapping = {"支持": "supported", "反驳": "refuted", "不足": "not_established"}
        self.assertEqual(prediction('{"verdict":"反驳","basis":"M1"}', mapping)["predicted_verdict"], "refuted")
        self.assertEqual(prediction('{"verdict":"refuted","basis":"M1"}', mapping)["predicted_verdict"], "invalid")

    def test_chinese_variant_keeps_claims_evidence_and_only_translates_instructions(self):
        specs = json.loads((ROOT / "datasets/controls/c_balanced_material_specs.json").read_text(encoding="utf-8"))
        payload, schemas = build_payload(specs)
        translated, zh_schemas = translate_payload(payload, schemas)
        for a, b in zip(payload["items"], translated["items"]):
            self.assertEqual(a["materials"], b["materials"])
            self.assertEqual(a["claim"], b["claim"])
            self.assertEqual(a["question"].split("\nM1：", 1)[1], b["question"].split("\nM1：", 1)[1])
            self.assertEqual(a["expected_fields"]["basis"], b["expected_fields"]["basis"])
        self.assertEqual(len(zh_schemas["schemas"]), 48)

    def test_imbalanced_or_tampered_position_gold_is_rejected(self):
        payload = json.loads((ROOT / "datasets/controls/c_balanced_materials_v1.json").read_text(encoding="utf-8"))
        validate_design(payload)
        payload["items"][0]["expected_fields"]["verdict"] = "refuted"
        with self.assertRaises(ValueError):
            validate_design(payload)
