"""Prepare-only C interface check; a model factory is forbidden from executing."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.governance.c_component import build_c_service
from src.utils.experiment_io import sha256_file

CASES = [
    ("hit", "2023年诺贝尔物理学奖授予了谁？", "time_sensitive", "hit", ["nobel-physics-2023"]),
    ("no_hit", "诺贝尔物理学奖得主“陈晓东”因为什么研究获奖？", "fictional_entity", "no_hit", []),
    ("math", "2023减1921等于多少？", "math_logic", "math_bypass", []),
    ("year_alias", "1921年度诺贝尔物理学奖实际在哪一年颁发？", "factual", "hit", ["nobel-einstein-1921"]),
    ("wrong_subject", "2023年诺贝尔文学奖得主“李华”的作品是什么？", "false_premise", "hit", ["nobel-literature-2023"]),
    ("normal", "只输出JSON对象，姓名小林，键为name。", "normal_control", "no_hit", []),
]


def check():
    def forbidden_model():
        raise AssertionError("Prepare-only contract check must never load a model")
    service, retriever, config = build_c_service(ROOT, forbidden_model)
    results = []
    for ident, question, category, expected_status, expected_ids in CASES:
        row = service.answer(question, config["strategy"], category, prepare_only=True)
        if row["retrieval_status"] != expected_status or [h["id"] for h in row["evidence"]] != expected_ids:
            raise ValueError("C interface retrieval contract differs: " + ident)
        if row["answer"] is not None or row["model_calls"] or row["answer_origin"] != "dry_run" or service.model is not None:
            raise ValueError("Prepared request incorrectly claims a model answer")
        if any(not h["source"].get("url") or not h["source"].get("accessed_at") for h in row["evidence"]):
            raise ValueError("Missing source provenance")
        if question not in row["prompt"]:
            raise ValueError("Original question lost")
        diagnostics = None if expected_status == "math_bypass" else retriever.search_with_diagnostics(question)
        if ident == "year_alias" and not diagnostics["query_expansion"]:
            raise ValueError("Effective retrieval query is not logged")
        results.append({"case": ident, "request": {"question": question, "category": category},
                        "prepared": row, "retrieval_diagnostics": diagnostics})
    return {"scope": "C_prepare_interface_only", "cases": results, "model_calls": 0, "passed": True,
            "profile_sha256": sha256_file(ROOT / "configs/c_component_profile.json"), "corpus_sha256": retriever.sha256}


if __name__ == "__main__":
    result = check()
    (ROOT / "docs/c_work/c_component_contract.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"passed": True, "cases": len(result["cases"]), "model_calls": 0}, ensure_ascii=False))
