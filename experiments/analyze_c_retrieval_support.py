"""C developer inspection of 30 evidence chains, not independent human scoring."""
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.governance.retrieval_scoped import AwardScopedRetrieverV2
from src.governance.retrieval_year_alias import AwardYearAliasRetriever
from src.utils.experiment_io import sha256_file

# Explicit AI developer judgments after reading the complete retrieved passages.
# These are evaluation-only annotations; neither retriever imports this module.
SPECS = {
    "1": ("no_retrieved_evidence", "无首都资料；不能把未命中等同回答错误。"),
    "3": ("supports_core", "ocean-01直接说明太平洋面积最大。"),
    "7": ("supports_core_with_scope", "个人记录证明获奖年度；重复获奖统计共同支持次数判断，保留1901—2025范围。"),
    "10": ("supports_core", "moon-01直接支持月球；earth-orbit只是地球背景，不支持卫星身份。"),
    "16": ("supports_core", "apollo-crew直接区分阿姆斯特朗、奥尔德林和柯林斯；moon-01不是人员证据。"),
    "17": ("supports_core", "trench-depth给出挑战者深渊属于马里亚纳海沟及世界最深处关系；不可把深渊改称海沟。"),
    "18": ("supports_core", "机械波片段直接说明声音需要介质；电磁波片段只提供对照。"),
    "27": ("supports_premise_correction_only", "年度公告支持福瑟获奖并可纠正题设身份；不支持李华的身份或代表作。"),
    "28": ("topic_only_insufficient", "相对论主题相关，但没有王明远身份或贡献资料；不能迁移爱因斯坦事迹。"),
    "29": ("no_retrieved_evidence", "无题设人物获奖资料；不证明该姓名人物不存在。"),
    "32": ("no_retrieved_evidence", "无该公司产品参数；不证明实体不存在。"),
    "38": ("no_retrieved_evidence", "指定2025年报未入检索库，不能声称据该报告已核实。"),
    "48": ("no_retrieved_evidence", "无题设人物化学奖资料，不支持获奖身份。"),
    "64": ("supports_core", "2023年度物理学奖名单与研究领域均在单条公告中。"),
    "66": ("supports_core", "2022年度物理学奖名单与研究领域均在单条公告中。"),
    "74": ("no_retrieved_evidence", "该库没有2020年度物理学奖记录，不应借2022/2023名单回答。"),
    "76": ("supports_core", "相对论史和狭义相对论片段指向爱因斯坦，足以纠正牛顿提出相对论的前提。"),
    "84": ("supports_core", "steam-history明确纽科门早于瓦特且瓦特为改进者；steam-use的1776—1778不是最初发明时间。"),
    "94": ("topic_only_insufficient", "灯史支持多位发明者的改进，未给牛顿生平或直接身份记录；不能据此编造人物介绍。"),
    "99": ("supports_core", "sun-01直接支持太阳不是行星且为太阳系唯一恒星；planets-01只能支持行星名单，不能列成恒星。"),
    "NP1": ("supports_core", "奖项片段支持光电效应与理论物理贡献；1922为颁发年，不是奖项年度。"),
    "NP2": ("supports_core", "1921年度记录直接给出爱因斯坦。"),
    "NP3": ("no_retrieved_evidence", "缺1922年度记录；不能借1921奖项在1922颁发来回答。"),
    "NP4": ("supports_core", "2023文学奖公告直接给出福瑟。"),
    "NP5": ("no_retrieved_evidence", "缺2024化学奖资料，年份和类别均不能借用其他记录。"),
    "NP6": ("supports_core", "2022与2023两条公告分别提供比较的两半；仅一条不能支持完整跨年比较。"),
    "BP1": ("retrieval_miss_with_available_evidence", "V2未命中，但库中1921记录明确写1922年颁发；年份别名回退可召回，这是检索漏检而非资料缺失。"),
    "BP2": ("supports_premise_correction_only", "年度记录支持福瑟身份和理由，不支持王明远获奖；只能纠正前提后介绍资料主体。"),
    "BP3": ("supports_core", "奖项记录给出光电效应工作，支持区分其与相对论的关系；不应把科学贡献全当颁奖理由。"),
    "BP4": ("supports_core", "同一年度同一主体记录中已有创新戏剧与散文的颁奖理由，不需要另行推测。"),
}


def main():
    data_path = ROOT / "docs/c_work/development_dataset.json"
    config_path = ROOT / "configs/c_evidence_binding.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    data = json.loads(data_path.read_text(encoding="utf-8"))
    items = [{k: x[k] for k in ("id", "question", "category")} for x in data["items"] if str(x["id"]) in SPECS] + config["probes"]
    if len(items) != 30 or {str(x["id"]) for x in items} != set(SPECS):
        raise ValueError("Inspection requires exactly the declared thirty exposed cases")
    corpus = ROOT / "knowledge/corpus_v4.json"
    before, after = AwardScopedRetrieverV2(corpus), AwardYearAliasRetriever(corpus)
    rows = []
    for item in items:
        label, note = SPECS[str(item["id"])]
        rows.append({**item, "inspection_origin": "AI_developer_not_independent_human", "support_judgment": label,
                     "basis": note, "v2_evidence": before.search(item["question"]),
                     "year_alias_diagnostics": after.search_with_diagnostics(item["question"])})
    payload = {"stage": "C_retrieval_failure_analysis_only", "formal_accuracy": None, "independent_human_reviews": 0,
               "cases": rows, "counts": dict(Counter(x["support_judgment"] for x in rows)),
               "inputs_sha256": {str(p.relative_to(ROOT)): sha256_file(p) for p in (data_path, config_path, corpus)},
               "runtime_sha256": {str(p.relative_to(ROOT)): sha256_file(p) for p in
                                   [Path(__file__), ROOT / "src/governance/retrieval.py", ROOT / "src/governance/retrieval_safe.py",
                                    ROOT / "src/governance/retrieval_scoped.py", ROOT / "src/governance/retrieval_year_alias.py"]}}
    target = ROOT / "docs/c_work/retrieval_support_30_v1.json"
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"cases": len(rows), "counts": payload["counts"], "independent_human_reviews": 0}, ensure_ascii=False))


if __name__ == "__main__":
    main()
