import unittest
from pathlib import Path
from src.governance.consistency import check_consistency
from src.governance.joint import JointGovernance
from src.governance.retrieval import LocalRetriever

ROOT = Path(__file__).resolve().parents[1]


class JointTests(unittest.TestCase):
    def service(self, hook=None):
        class Model:
            last_generation = {"input_tokens": 1, "output_tokens": 2, "truncated": False}
            def generate(self, prompt, **kwargs):
                return "原始回答[bogus]"
        return JointGovernance(LocalRetriever(ROOT / "knowledge/corpus_v3.json"), Model, hook, "fixture-v1" if hook else None)

    def test_raw_answer_preserved_and_unknown_citation_reported(self):
        row = self.service().answer("真空光速是多少？", bias_mode="prompt")
        self.assertEqual(row["answer"], "原始回答[bogus]")
        self.assertIn("unknown_citation", [f["code"] for f in row["consistency"]["flags"]])
        self.assertEqual(row["model_calls"], 1)

    def test_hook_failure_does_not_silently_generate_without_bias_stage(self):
        def fail(prompt):
            raise RuntimeError("fixture failure")
        row = self.service(fail).answer("问题", bias_mode="hook")
        self.assertEqual((row["status"], row["model_calls"]), ("error", 0))
        self.assertIsNone(row["answer"])

    def test_guarded_program_answer_is_not_claimed_as_joint_model_inference(self):
        row = self.service().answer("中国的首都是哪个城市？", strategy="guarded", bias_mode="prompt")
        self.assertEqual((row["answer_origin"], row["model_calls"]), ("policy_abstention", 0))

    def test_numeric_citation_mapping_is_respected(self):
        result = check_consistency("结果[1]", [{"id": "a"}], {"1": "a"})
        self.assertEqual(result["flags"], [])
        self.assertIsNone(result["factual_accuracy"])

    def test_material_field_conflicts_are_mechanical(self):
        r = check_consistency('{"verdict":"不足","basis":"M3"}', materials=[{"id": "M1"}, {"id": "M2"}])
        self.assertEqual({f["code"] for f in r["flags"]}, {"insufficient_with_selected_basis", "basis_outside_supplied_materials"})

    def test_hypothetical_numbers_are_only_screening_not_factual_errors(self):
        r = check_consistency("无法核实；例如售价100元只是一个假设。")
        self.assertEqual(r["flags"][0]["kind"], "screening")
        self.assertIsNone(r["factual_accuracy"])

    def test_invalid_hook_configuration_is_rejected(self):
        with self.assertRaises(ValueError):
            JointGovernance(None, None, bias_hook=lambda p: p)

    def test_hook_cannot_silently_erase_c_evidence(self):
        row = self.service(lambda p: "删除了原始问题和证据").answer("真空光速是多少？", bias_mode="hook")
        self.assertEqual((row["status"], row["model_calls"]), ("error", 0))

    def test_material_citation_is_not_mistaken_for_missing_rag_citation(self):
        result = check_consistency("判断见[M1]", materials=[{"id": "M1"}])
        self.assertEqual(result["flags"], [])
