"""Exploratory label-wording follow-up: translate enum labels without changing evidence or claims."""
import argparse
import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.utils.experiment_io import sha256_file

TO_ZH = {"supported": "支持", "refuted": "反驳", "not_established": "不足"}


def translate_payload(payload, schemas):
    result, schema_result = copy.deepcopy(payload), copy.deepcopy(schemas)
    result.update(version="c-balanced-materials-cn-v1", label_language="zh",
                  label_to_canonical={v: k for k, v in TO_ZH.items()},
                  followup_scope="看到英文标签偏向后追加的探索性措辞对照，不属于原预先评分计划。")
    for item in result["items"]:
        # Replace the instruction block only; material text and the target statement are immutable.
        instructions, body = item["question"].split("\nM1：", 1)
        for old, new in TO_ZH.items():
            instructions = instructions.replace(old, new)
        item["question"] = instructions + "\nM1：" + body
        item["expected_fields"]["verdict"] = TO_ZH[item["expected_fields"]["verdict"]]
    result["design"]["expected_verdict_counts"] = {TO_ZH[k]: v for k, v in result["design"]["expected_verdict_counts"].items()}
    schema_result["version"] = "c-balanced-material-cn-schemas-v1"
    for schema in schema_result["schemas"].values():
        schema["fields"][0]["values"] = [TO_ZH[v] for v in schema["fields"][0]["values"]]
    return result, schema_result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    output = ROOT / "datasets/controls/c_balanced_materials_cn_v1.json"
    schema_output = ROOT / "configs/c_balanced_material_schemas_cn_v1.json"
    protocol_output = ROOT / "docs/c_work/balanced_label_followup_v1.json"
    if any(p.exists() for p in (output, schema_output, protocol_output)):
        raise FileExistsError("Publish new paths instead of rewriting a label follow-up")
    data_path = ROOT / "datasets/controls/c_balanced_materials_v1.json"
    schemas_path = ROOT / "configs/c_balanced_material_schemas_v1.json"
    payload, schemas = translate_payload(json.loads(data_path.read_text(encoding="utf-8")), json.loads(schemas_path.read_text(encoding="utf-8")))
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    schema_output.write_text(json.dumps(schemas, ensure_ascii=False, indent=2), encoding="utf-8")
    paths = [data_path, schemas_path, output, schema_output, ROOT / "configs/c_balanced_materials_cn.json",
             ROOT / "datasets/controls/c_balanced_material_specs.json"]
    protocol = {"stage": "exploratory_label_wording_followup_declared_before_zh_inference",
                "trigger": "原英文条件明显集中输出supported，因此只更换指令和值域中的状态标签。",
                "changes": "supported/refuted/not_established改为支持/反驳/不足；材料、陈述、顺序、依据编号、种子和解码预算不变。",
                "planned_outputs": 192, "independent_human_reviews": 0,
                "scoring": "中文输出按固定公开映射归一化后比较结论、依据、两者同时正确、位置交换；无效标签另列。",
                "limits": "探索性追加，不能冒充原预注册计划；标签翻译也改变token及语言先验，不据此断言模型内部机制。",
                "frozen_input_sha256": {p.relative_to(ROOT).as_posix(): sha256_file(p) for p in paths}}
    protocol_output.write_text(json.dumps(protocol, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Frozen 48 translated-label variants and follow-up plan; evidence and statements unchanged")


if __name__ == "__main__":
    main()
