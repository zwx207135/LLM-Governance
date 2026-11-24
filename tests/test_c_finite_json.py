import copy
import json
import unittest
from pathlib import Path

from experiments.run_c_structured_comparison import generation_tasks
from src.governance.finite_json import FiniteJsonConstraint, allowed_outputs

ROOT = Path(__file__).resolve().parents[1]


class CharacterTokenizer:
    def encode(self, text, add_special_tokens=False):
        return [ord(c) for c in text]

    def decode(self, tokens, skip_special_tokens=False):
        return "".join(chr(t) for t in tokens)


class FiniteJsonTests(unittest.TestCase):
    def setUp(self):
        self.schema = {"fields": [{"name": "recorded", "values": [True, False]},
                                  {"name": "identity", "values": ["supported", "refuted", "not_established"]}]}
        self.outputs = allowed_outputs(self.schema)
        self.constraint = FiniteJsonConstraint(CharacterTokenizer(), self.outputs, 2, [99999], 192)

    def test_all_six_semantic_combinations_survive(self):
        self.assertEqual(len(self.outputs), 6)
        pairs = {(r["recorded"], r["identity"]) for r in map(json.loads, self.outputs)}
        self.assertEqual(pairs, {(v, label) for v in (True, False) for label in ("supported", "refuted", "not_established")})

    def test_every_complete_path_allows_eos_and_no_prefix_can_end_early(self):
        for output in self.outputs:
            ids = [ord(c) for c in output]
            for length, token in enumerate(ids):
                allowed = self.constraint.allowed_tokens(0, [7, 8] + ids[:length])
                self.assertIn(token, allowed)
                self.assertNotIn(99999, allowed)
            self.assertEqual(self.constraint.allowed_tokens(0, [7, 8] + ids), [99999])

    def test_invalid_prefix_cannot_escape_to_unconstrained_generation(self):
        with self.assertRaises(ValueError):
            self.constraint.allowed_tokens(0, [7, 8, ord("x")])
        with self.assertRaises(ValueError):
            self.constraint.allowed_tokens(1, [7, 8])

    def test_insufficient_budget_is_rejected_instead_of_returning_partial_json(self):
        with self.assertRaises(ValueError):
            FiniteJsonConstraint(CharacterTokenizer(), self.outputs, 2, [99999], 3)

    def test_gold_fields_are_rejected_from_schema(self):
        with self.assertRaises(ValueError):
            allowed_outputs({**self.schema, "expected_fields": {"recorded": True}})

    def test_duplicate_fields_values_and_excessive_language_size_are_rejected(self):
        for schema in ({"fields": [self.schema["fields"][0]] * 2},
                       {"fields": [{"name": "x", "values": [True, True]}]},
                       {"fields": [{"name": "x", "values": list(map(str, range(65)))}]},
                       {"fields": [{"name": "x", "values": [1, 2]}]}):
            with self.assertRaises(ValueError):
                allowed_outputs(schema)

    def test_changing_gold_does_not_change_generation_inputs_or_allowed_outputs(self):
        payload = json.loads((ROOT / "datasets/controls/c_source_bound_development.json").read_text(encoding="utf-8"))
        schemas = json.loads((ROOT / "configs/c_source_bound_schemas.json").read_text(encoding="utf-8"))["schemas"]
        before = generation_tasks(payload, schemas)
        changed = copy.deepcopy(payload)
        for item in changed["items"]:
            item["expected_fields"] = {"deliberately_wrong_gold": "TEST_ONLY"}
            item["reference"] = "TEST_ONLY_DO_NOT_SEND"
        self.assertEqual(generation_tasks(changed, schemas), before)
        self.assertTrue(all(len(values) == 6 for values in before[1].values()))
        self.assertTrue(all(set(task) == {"id", "question", "category"} for task in before[0]))

    def test_real_schema_outputs_roundtrip_as_exact_json_types(self):
        schemas = json.loads((ROOT / "configs/c_source_bound_schemas.json").read_text(encoding="utf-8"))["schemas"]
        for schema in schemas.values():
            outputs = allowed_outputs(schema)
            self.assertEqual(len(outputs), 6)
            for output in outputs:
                value = json.loads(output)
                self.assertIs(type(value[schema["fields"][0]["name"]]), bool)
                self.assertIs(type(value[schema["fields"][1]["name"]]), str)
