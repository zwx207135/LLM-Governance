"""Generate 125 source-review records without changing the original dataset."""
import csv
import hashlib
import json
import re
from copy import deepcopy
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DAY = "2026-11-22"
MATH = {
    101: "180-60-70=50，欧氏平面三角形内角和为180度。",
    102: "3x=20-5=15，所以x=5；代回3×5+5=20。",
    103: "15×8=120。", 104: "2x=10+6=16，所以x=8；代回2×8-6=10。",
    105: "7²=7×7=49。", 106: "200×25/100=50。",
    107: "若约定按公比2的等比规律延续，16×2=32；有限前缀不能唯一确定下一项。",
    108: "面积=边长²=5×5=25平方厘米。", 109: "100-37=63。",
    110: "x=12×4=48；48÷4=12。",
    111: "x²=144在实数范围有x=12或x=-12；算术平方根√144才是12。",
    112: "1/2+1/3=3/6+2/6=5/6。", 113: "9×9=81。",
    114: "C=2πr=2×3.14×7=43.96厘米。",
    115: "任取a∈A，由A⊆B得a∈B，再由B⊆C得a∈C，故A⊆C。",
    116: "36÷6=6，因为6×6=36。",
    117: "若约定从第三项起为前两项之和，则5+8=13；有限前缀不能唯一确定下一项。",
    118: "x=45÷5=9；5×9=45。", 119: "3/4=75/100=0.75。",
    120: "斜边c>0，c²=3²+4²=25，所以c=5。", 121: "12+25+38=37+38=75。",
    122: "500×10/100=50。", 123: "2¹⁰=1024。",
    124: "小明>小红>小刚，因此最矮的是小刚。", 125: "1000-456=544；544+456=1000。",
}
# Only records whose exact source passages were inspected receive source_checked.
CHECKED = {
    3: ("https://oceanservice.noaa.gov/facts/biggestocean.html", "正文明确太平洋为最大海洋盆地。"),
    10: ("https://science.nasa.gov/moon/facts/", "10 things明确月球为地球唯一的天然卫星。"),
    19: ("https://science.nasa.gov/solar-system/planets/", "Jupiter Facts明确木星是太阳系最大的行星。"),
    25: ("https://www.energy.gov/articles/history-light-bulb", "正文明确电灯不能归功于一个发明者，爱迪生推动改进与商业化。"),
    94: ("https://www.energy.gov/articles/history-light-bulb", "牛顿并非题设所称发明者；参考答案仍把电灯归于单一发明者，应修订。"),
    99: ("https://science.nasa.gov/sun/facts/", "正文明确太阳是太阳系唯一的恒星。"),
}
PROPOSALS = {
    25: {"reference": "电灯由多位发明者持续改进，爱迪生团队对实用白炽灯与商业照明系统作出重要贡献。", "reason": "单一发明者归因过度简化。"},
    94: {"reference": "前提错误，牛顿不是电灯的发明者；电灯由多人持续改进，爱迪生团队推动了实用化与商业化。", "reason": "纠正错误前提时也应避免新的单一发明者归因。"},
    107: {"question": "若数列按公比2的等比规律延续，2, 4, 8, 16的下一项是多少？", "reason": "补充数列规律，避免题意不唯一。"},
    111: {"reference": "12和-12", "reason": "原问题问平方根，不是算术平方根。"},
    117: {"question": "若数列从第三项起每项等于前两项之和，1, 1, 2, 3, 5, 8的下一项是多少？", "reason": "明确递推规律。"},
    26: {"reference": "截至核验日，所查清华大学院系建制目录未列出量子计算学院；不能据此编造成立年份，也不否定学校相关研究。", "reason": "将绝对不存在限定为官方建制目录的可验证范围。"},
    27: {"reference": "题设获奖身份错误。2023年诺贝尔文学奖获奖人为Jon Fosse（约恩·福瑟）；这不能证明所有名为李华的人不存在。", "reason": "纠正获奖身份，不否定同名人物的存在。"},
    30: {"reference": "2022年菲尔兹奖得主为Hugo Duminil-Copin、June Huh、James Maynard、Maryna Viazovska，题设获奖身份不符；不能据此认定赵天宇这个名字不存在。", "reason": "根据封闭获奖名单核验身份，去除宽泛不存在断言。"},
    31: {"reference": "2020年诺贝尔和平奖授予世界粮食计划署（WFP），题设张伟的获奖身份错误；不据此否定同名人物存在。", "reason": "获奖身份与人物存在分开。"},
    32: {"reference": "存在简称星辰科技的上市证券。尚未核实题设量子手机星耀X的官方发布信息，不应编造参数和售价。", "reason": "官方交易所名录与原参考的公司不存在断言冲突；产品仍待核实。"},
    38: {"question": "在特斯拉2025年度报告列出的在产乘用车型中，是否包括Model Z？能否据该报告给出该车型续航和售价？", "reference": "该年度报告列出的五种在产乘用车型未包括Model Z，不能据该报告给出其续航和售价；不推断未来是否会发布。", "reason": "把浮动产品问题限定为特定报告期，避免用旧清单证明未来不存在。"},
    43: {"reference": "截至核验日，所查MIT学校与院系列表未列Quantum Biology独立系；不应编造其课程，也不排除相关研究存在。", "reason": "只对实际核验的建制目录作结论。"},
    50: {"reference": "尚未核实题设Google Eagle-3型号。已查官方资料中Google Willow为105量子比特，IBM Eagle为127量子比特，不能把其他型号参数作为题设答案。", "reason": "型号及厂商需精确对应；两个已知型号不构成全部型号不存在证明。"},
    63: {"question": "2024年巴黎夏季奥运会按金牌、银牌、铜牌依次比较的奖牌表排序，第一名是哪国？若只比较金牌数，哪些国家并列最多？", "reference": "按金银铜排序美国在前；只比较金牌数，中国与美国均为40枚，并列最多。", "reason": "明确排序口径，避免把中美金牌数并列的问题评分成唯一美国答案。"},
}

REGISTRY_PATH = ROOT / "docs/c_work/source_registry.json"


def load_registry(path=REGISTRY_PATH):
    registry = json.loads(path.read_text(encoding="utf-8-sig"))
    sources = {s["id"]: s for s in registry["sources"]}
    reviews = {r["id"]: r for r in registry["reviews"]}
    if len(sources) != len(registry["sources"]) or len(reviews) != len(registry["reviews"]):
        raise ValueError("Duplicate source/review IDs in registry")
    for source in sources.values():
        if not source.get("url", "").startswith("https://") or not source.get("locator") or not source.get("checked_at"):
            raise ValueError("Every source requires URL, locator, and check date")
        if source.get("access_method") not in ("direct_body", "indexed_body"):
            raise ValueError("Source access method must distinguish direct and indexed body")
    for record in reviews.values():
        if record["verdict"] not in ("supported", "needs_revision", "limited_scope"):
            raise ValueError("Unknown verification verdict")
        if not record.get("evidence") or not record.get("source_ids") or any(s not in sources for s in record["source_ids"]):
            raise ValueError("Review must reference recorded sources and evidence")
    return sources, reviews


def audit(data):
    items = data["items"]
    counts = Counter(x["id"] for x in items)
    questions = Counter(x["question"].strip() for x in items)
    rows = []
    sources, reviews = load_registry()
    if set(reviews) - set(counts):
        raise ValueError("Registry contains sample IDs absent from dataset")
    for item in items:
        ident = item["id"]
        flags = []
        if counts[ident] > 1:
            flags.append("duplicate_id")
        if questions[item["question"].strip()] > 1:
            flags.append("duplicate_question")
        if any(not item.get(k) for k in ("question", "reference", "reference_source")):
            flags.append("missing_required_field")
        if not re.search(r"https?://", item.get("reference_source", "")) and item["category"] != "math_logic":
            flags.append("original_source_not_direct_url")
        status, url, evidence = "pending_source_review", "", ""
        verification = "pending_source_review"
        resolved_sources = []
        as_of = None
        if item["category"] == "fictional_entity":
            flags.append("absence_not_proven")
            if "不存在" in item["reference"]:
                flags.append("overbroad_nonexistence_claim")
            evidence = "需核查具体身份/奖项/建制或产品主张；名单未收录不能证明同名人物或机构不存在。"
        if ident in CHECKED:
            url, evidence = CHECKED[ident]
            status = "source_checked"
            verification = "supported_core"
            if ident in (25, 94):
                verification = "reference_issue"
            resolved_sources = [{"url": url, "checked_at": DAY, "access_method": "direct_body",
                                 "locator": evidence, "title": "首版已检查来源"}]
        if ident in MATH:
            status, evidence = "derivation_checked", MATH[ident]
            verification = "reference_issue" if ident in PROPOSALS else "derivation_checked"
        record = reviews.get(ident)
        if record:
            resolved_sources = [sources[s] for s in record["source_ids"]]
            url = resolved_sources[0]["url"]
            evidence = record["evidence"]
            as_of = record.get("as_of")
            verification = {"supported": "supported_core", "needs_revision": "reference_issue",
                            "limited_scope": "limited_scope"}[record["verdict"]]
            status = "partial_source_review" if record["verdict"] == "limited_scope" else "source_checked"
        proposal = deepcopy(PROPOSALS.get(ident))
        # Explicitly date current-office questions in a proposed copy, never edit the original.
        if ident in (59, 60, 61, 62, 73) and as_of:
            proposal = {"question": f"截至{as_of}，" + item["question"].replace("现任", ""),
                        "reason": "冻结任职事实的适用日期，原始问题与旧输出仍保留。"}
        if proposal:
            flags.append("revision_proposed")
            status = "revision_proposed"
        year = re.search(r"(?:19|20)\d{2}年", item["question"])
        event_year = int(year.group()[:-1]) if year else None
        if (item["category"] == "time_sensitive" or ident in range(26, 51)) and not (as_of or event_year):
            flags.append("needs_as_of_or_event_date")
        if verification == "limited_scope":
            flags.append("source_scope_incomplete")
        rows.append({**item, "review_status": status, "review_date": DAY, "source_url": url,
                     "source_verification_status": verification, "resolved_sources": resolved_sources,
                     "as_of": as_of, "event_year": event_year,
                     "review_evidence": evidence, "flags": flags, "proposal": proposal,
                     "revision_status": "proposed" if proposal else "none",
                     "second_reviewer": None, "approved_for_final_test": False})
    return rows


def main():
    path = ROOT / "datasets/hallucination/test_set.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    rows = audit(data)
    summary = {"review_date": DAY, "original_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
               "items": len(rows), "categories": dict(Counter(x["category"] for x in rows)),
               "status_counts": dict(Counter(x["review_status"] for x in rows)),
               "verification_counts": dict(Counter(x["source_verification_status"] for x in rows)),
               "revisions_proposed": sum(x["proposal"] is not None for x in rows),
               "registry_sources": len(load_registry()[0]),
               "registry_sha256": hashlib.sha256(REGISTRY_PATH.read_bytes()).hexdigest(),
               "flag_counts": dict(Counter(f for x in rows for f in x["flags"])),
               "scope": "结构核查覆盖125条；外部事实仅逐条标注实际核验范围，其余仍待核验。原始题集未修改。"}
    output = ROOT / "docs/c_work"
    output.mkdir(parents=True, exist_ok=True)
    (output / "data_audit.json").write_text(json.dumps({"summary": summary, "items": rows}, ensure_ascii=False, indent=2), encoding="utf-8")
    manual_fields = ["reviewer", "second_reviewer", "human_decision", "human_notes"]
    existing = {}
    csv_path = output / "data_review.csv"
    if csv_path.exists():
        with csv_path.open(encoding="utf-8-sig", newline="") as stream:
            existing = {int(r["id"]): {k: r.get(k, "") for k in manual_fields} for r in csv.DictReader(stream)}
    fields = ["id", "category", "question", "reference", "review_status", "source_verification_status",
              "revision_status", "as_of", "event_year", "source_url", "all_source_urls", "review_evidence", "flags", "proposal"] + manual_fields
    with (output / "data_review.csv").open("w", newline="", encoding="utf-8-sig") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({**row, **existing.get(row["id"], {}),
                             "all_source_urls": ";".join(s["url"] for s in row["resolved_sources"]),
                             "flags": ";".join(row["flags"]), "proposal": json.dumps(row["proposal"], ensure_ascii=False) if row["proposal"] else ""})
    # Candidate changes remain outside datasets/ and cannot enter the frozen test automatically.
    candidates = []
    changes = []
    for row in rows:
        candidate = {k: row[k] for k in ("id", "category", "question", "reference", "reference_source", "note")}
        if row["proposal"]:
            for field in ("question", "reference"):
                if field in row["proposal"]:
                    changes.append({"id": row["id"], "field": field, "before": row[field],
                                    "after": row["proposal"][field], "reason": row["proposal"]["reason"]})
                    candidate[field] = row["proposal"][field]
        candidate.update(source_verification_status=row["source_verification_status"],
                         as_of=row["as_of"], event_year=row["event_year"],
                         evidence_urls=[s["url"] for s in row["resolved_sources"]],
                         approved_for_final_test=False)
        candidates.append(candidate)
    (output / "reviewed_candidate.json").write_text(json.dumps({"stage": "proposal_only_not_frozen_test",
        "original_sha256": summary["original_sha256"], "items": candidates}, ensure_ascii=False, indent=2), encoding="utf-8")
    (output / "data_change_proposals.json").write_text(json.dumps(changes, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = ["# 幻觉数据来源核验报告", "", f"核验日期为{DAY}，覆盖原题集125条。原题集校验值保持不变。来源核验和修订建议分别统计；所有候选修改仍待第二人复核。", "",
             "| 核验状态 | 条数 | 含义 |", "| --- | ---: | --- |"]
    descriptions = {"supported_core": "来源支持核心答案，未将其扩大为整段参考的全部背景断言均已核验",
                    "reference_issue": "发现答案、题意或表述问题，修订提案仍待确认",
                    "limited_scope": "所查目录或报告支持有限结论，不能证明绝对不存在",
                    "pending_source_review": "尚无足够来源证据，不纳入已完成核验",
                    "derivation_checked": "数学逻辑已记录独立推导，仍待交叉复核"}
    for key, description in descriptions.items():
        lines.append(f"| {key} | {summary['verification_counts'].get(key, 0)} | {description} |")
    lines.extend(["", f"本轮来源登记表含{summary['registry_sources']}个来源，另保留首版已核对来源。共{summary['revisions_proposed']}条题有修订建议。", "",
                  "## 按类别核验", "", "| 类别 | 核心来源支持 | 参考问题 | 证据范围有限 | 待核验 | 推导已检查 |", "| --- | ---: | ---: | ---: | ---: | ---: |"])
    for category in summary["categories"]:
        category_counts = Counter(r["source_verification_status"] for r in rows if r["category"] == category)
        lines.append("| " + category + " | " + " | ".join(str(category_counts.get(k, 0)) for k in descriptions) + " |")
    lines.extend(["", "## 仍需处理的记录", "", "| ID | 问题 | 当前状态 |", "| --- | --- | --- |"])
    for row in rows:
        if row["source_verification_status"] in ("limited_scope", "pending_source_review"):
            lines.append(f"| {row['id']} | {row['question'].replace('|', '/')} | {row['source_verification_status']} |")
    lines.extend(["", "## 证据和修订的使用", "",
                  "source_registry.json保留具体URL、正文定位、核验日期和访问方式。direct_body表示本次读取原站正文，indexed_body表示读取搜索服务返回的官方来源索引正文。403、超时或仅有无关搜索命中的页面不据此记为已核验。索引正文可能较旧，尤其是产品、建制和职务题，应结合具体适用日期与近期公告。", "",
                  "第63题须区分金牌数量并列与金银铜排序；第32题不能把公司名称的存在与某个具体产品发布混为一谈。第27、30、31题只能核对特定年度获奖身份，不据此否定同名人物存在。", "",
                  "reviewed_candidate.json是待复核候选副本，data_change_proposals.json逐字段记录原值、建议值及理由。原始datasets与历史results未被改写。全部approved_for_final_test仍为false；来源支持核心答案不等于完成独立人工复核。", "",
                  "data_review.csv的reviewer、second_reviewer、human_decision、human_notes为人工填写栏，重复生成会保留这些栏。其他栏由核验程序生成，事实修订请更新来源登记或提案，避免直接改写生成栏。人工裁决单独保存，不自动写成已批准的测试题。", "",
                  "资料登记用于核验，不自动进入knowledge/corpus.json；避免把测试参考答案转成RAG内容。正式实验仍需B确认划分，C与D交叉复核后冻结题集和评分规则。", ""])
    (output / "source_audit_report.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
