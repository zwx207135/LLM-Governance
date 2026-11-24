import json
import tempfile
import unittest
from pathlib import Path

from src.governance.c_component import load_profile
from experiments.check_c_component_contract import check

ROOT = Path(__file__).resolve().parents[1]


class ComponentProfileTests(unittest.TestCase):
    def test_contract_uses_no_model(self):
        self.assertEqual(check()["model_calls"], 0)

    def test_wrong_hash_and_reference_input_are_rejected(self):
        original = json.loads((ROOT / "configs/c_component_profile.json").read_text(encoding="utf-8"))
        for change in ({"corpus_sha256": "bad"}, {"reference": "must not enter"}, {"min_score": float("nan")}):
            with tempfile.TemporaryDirectory() as folder:
                path = Path(folder) / "profile.json"
                path.write_text(json.dumps({**original, **change}), encoding="utf-8")
                with self.assertRaises(ValueError): load_profile(ROOT, path)


if __name__ == "__main__":
    unittest.main()
