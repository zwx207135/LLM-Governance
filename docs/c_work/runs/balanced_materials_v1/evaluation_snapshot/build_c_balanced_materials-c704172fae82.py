"""Freeze balanced material judgments and counterbalanced evidence-position pairs."""
import argparse
import json
import random
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from experiments.evaluate_c_reviews import sources
from src.utils.experiment_io import sha256_file

LABELS = ("supported", "refuted", "not_established")
INSTRUCTIONS = """只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。
"""


def build_payload(specs, seed=20261122):
    topics = {t["id"]: t for t in specs["topics"]}
    if len(topics) != 8 or len(topics) != len(specs["topics"]):
        raise ValueError("This balanced version requires eight distinct topic groups")
    cases = []
    for number, topic in enumerate(topics.values()):
        if set(topic["claims"]) != set(LABELS) or topic["distractor_topic"] not in topics or topic["distractor_topic"] == topic["id"]:
            raise ValueError("Every topic needs all three claims and a distinct distractor")
        distractor = topics[topic["distractor_topic"]]
        for label in LABELS:
            relevant_first = (number + (label == "refuted")) % 2 == 0
            pair_materials = [topic, distractor] if relevant_first else [distractor, topic]
            cases.append({"topic": topic, "label": label, "materials": pair_materials})
    rng = random.Random(seed)
    rng.shuffle(cases)
    items, schemas = [], {}
    for number, case in enumerate(cases, 1):
        pair_id = f"P{number:02d}"
        for variant in ("base", "swapped"):
            ordered = case["materials"] if variant == "base" else list(reversed(case["materials"]))
            materials = [{"id": f"M{i}", "text": t["material"], "source_ids": t["source_ids"]} for i, t in enumerate(ordered, 1)]
            ident = pair_id + ("a" if variant == "base" else "b")
            basis = "none" if case["label"] == "not_established" else f"M{ordered.index(case['topic']) + 1}"
            claim = case["topic"]["claims"][case["label"]]
            question = INSTRUCTIONS + "\n" + "\n".join(f"{m['id']}：{m['text']}" for m in materials) + "\n\n目标陈述：" + claim
            items.append({"id": ident, "category": "normal_control", "question": question,
                          "contrast_group": case["topic"]["id"], "topic_name": case["topic"]["name"],
                          "case_pair_id": pair_id, "position_variant": variant, "claim": claim, "materials": materials,
                          "expected_fields": {"verdict": case["label"], "basis": basis},
                          "source_ids": sorted({s for m in materials for s in m["source_ids"]}),
                          "review_checklist": "仅对给定材料推理，反驳需要具体冲突；不足不能当作不存在。"})
            schemas[ident] = {"fields": [{"name": "verdict", "values": list(LABELS)},
                                         {"name": "basis", "values": ["M1", "M2", "none"]}]}
    rng.shuffle(items)
    return {"version": "c-balanced-materials-v1", "stage": "developer_authored_not_independent_test",
            "design": {"topics": 8, "unique_claims": 24, "position_variants_per_claim": 2, "questions": 48,
                       "expected_verdict_counts": dict(Counter(i["expected_fields"]["verdict"] for i in items)),
                       "expected_basis_counts": dict(Counter(i["expected_fields"]["basis"] for i in items)),
                       "seed": seed, "independence_unit": "eight topic groups; variants and contrast claims are related"},
            "items": items}, {"version": "c-balanced-material-schemas-v1", "schemas": schemas}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "datasets/controls/c_balanced_materials_v1.json")
    parser.add_argument("--schemas", type=Path, default=ROOT / "configs/c_balanced_material_schemas_v1.json")
    args = parser.parse_args()
    if args.output.exists() or args.schemas.exists():
        raise FileExistsError("Use new versioned paths; frozen material diagnostics are retained")
    spec_path = ROOT / "datasets/controls/c_balanced_material_specs.json"
    specs = json.loads(spec_path.read_text(encoding="utf-8"))
    valid_sources = sources()
    if any(s not in valid_sources for t in specs["topics"] for s in t["source_ids"]):
        raise ValueError("Material sources must be registered")
    payload, schemas = build_payload(specs)
    payload["source_specs_sha256"] = sha256_file(spec_path)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    args.schemas.write_text(json.dumps(schemas, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(payload["design"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
