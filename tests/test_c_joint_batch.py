import unittest
from pathlib import Path
from src.governance.consistency_v2 import check_consistency_v2, validate_materials
from src.governance.joint_batch import JointBatchService
from src.governance.retrieval import LocalRetriever
from experiments.run_c_joint_batch import validate

ROOT = Path(__file__).resolve().parents[1]


class JointBatchTests(unittest.TestCase):
    def test_materials_are_in_actual_prompt_and_audit_context(self):
        prompts = []
        class Model:
            last_generation = {"output_tokens": 2}
            def generate(self, prompt, **kwargs):
                prompts.append(prompt)
                return "资料[M1]"
        s = JointBatchService(LocalRetriever(ROOT / "knowledge/corpus_v3.json"), Model)
        row = s.answer("提取材料", category="normal_control", materials=[{"id": "M1", "text": "独特材料XYZ"}])
        self.assertIn("独特材料XYZ", prompts[0])
        self.assertEqual(row["consistency_v2"]["flags"], [])

    def test_duplicate_materials_or_gold_fields_are_rejected(self):
        for m in ([{"id": "M1", "text": "x"}] * 2, [{"id": "M1", "text": "x", "reference": "gold"}]):
            with self.assertRaises(ValueError):
                validate_materials(m)

    def test_exact_quote_presence_does_not_claim_entailment(self):
        r = check_consistency_v2('{"quote":"太阳","basis":"M1"}', materials=[{"id": "M1", "text": "太阳是恒星"}])
        self.assertEqual(r["quote_support"], "exact_substring_present")
        self.assertEqual(r["semantic_support"], "not_evaluated")

    def test_quote_in_different_material_is_not_passed(self):
        r = check_consistency_v2('{"quote":"月球","basis":"M1"}', materials=[{"id": "M1", "text": "太阳"}, {"id": "M2", "text": "月球"}])
        self.assertEqual(r["flags"][-1]["code"], "quote_not_in_selected_material")

    def test_nonfinite_json_and_invalid_verdict_are_flagged(self):
        self.assertIn("nonfinite_json_constant", [f["code"] for f in check_consistency_v2('{"value":NaN}')["flags"]])
        self.assertIn("invalid_verdict_value", [f["code"] for f in check_consistency_v2('{"verdict":true}')["flags"]])

    def test_batch_rejects_reference_leakage_and_unknown_modes(self):
        c = {"conditions": [{"name": "a", "strategy": "combined", "bias_mode": "off"}], "max_new_tokens": 192}
        with self.assertRaises(ValueError):
            validate(c, [{"id": 1, "question": "Q", "reference": "gold"}])
        c["conditions"][0]["bias_mode"] = "unknown"
        with self.assertRaises(ValueError):
            validate(c, [{"id": 1, "question": "Q"}])

    def test_duplicate_json_keys_cannot_produce_a_successful_quote_check(self):
        r = check_consistency_v2('{"quote":"不存在","quote":"太阳","basis":"M1"}', materials=[{"id": "M1", "text": "太阳是恒星"}])
        self.assertEqual(r["quote_support"], "not_evaluated")
        self.assertIn("unparseable_structured_answer", [f["code"] for f in r["flags"]])
