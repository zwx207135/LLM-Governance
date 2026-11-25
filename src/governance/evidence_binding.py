"""Source-linked reading aids; no reference inputs and no generated answer overrides."""
import re

from src.governance.anti_hallucination import AntiHallucination
from src.governance.retrieval_safe import anchor_matches

POLICIES = ("combined", "binding_cards")


def evidence_cards(question, evidence):
    quoted = re.findall(r'[“「『"]([^”」』"]{1,80})[”」』"]', question)
    cards = []
    for hit in evidence:
        scope = hit.get("scope", {})
        if scope.get("kind") not in ("award_record", "award_statistics"):
            continue
        # Every field is traceable to curated metadata or an exact text span.
        # A literal non-match is not an identity judgment or proof of absence.
        card = {"chunk_id": hit["id"], "source_id": hit["source_id"], "scope_origin": "curated_source_metadata",
                "award_year": scope.get("award_year"), "through_year": scope.get("through_year"),
                "subject_aliases": list(scope.get("subject_aliases", [])), "quoted_checks": [], "text_fields": []}
        if scope.get("kind") == "award_record":
            for name in quoted:
                matches = [a for a in card["subject_aliases"] if anchor_matches(a, name)]
                card["quoted_checks"].append({"quoted_text": name, "matching_aliases": matches,
                                               "status": "literal_match" if matches else "not_matched_in_this_record"})
            for match in re.finditer(r"(?:于|在)((?:19|20)\d{2})年颁发", hit["text"]):
                card["text_fields"].append({"field": "conferred_year", "value": int(match.group(1)),
                                            "exact_quote": match.group(0), "start": match.start(), "end": match.end()})
        cards.append(card)
    return cards


def render_cards(cards):
    lines = ["资料阅读对照（只描述下方资料，不是题设事实或最终答案）：",
             "区分问题给出的姓名和资料记载的主体。未匹配到引号内容时，不把资料中其他人的事迹转给它；这不能证明该姓名的人不存在。",
             "奖项年度与实际颁发年份分别回答，不互相替换。保留资料范围，不把这些提示当作额外来源。"]
    for card in cards:
        lines.append(f"资料[{card['chunk_id']}]：")
        if card["subject_aliases"]:
            lines.append("该资料记载的主体别名：" + "、".join(card["subject_aliases"]))
        if card["award_year"] is not None:
            lines.append(f"奖项年度（资料元数据）：{card['award_year']}年。")
        if card["through_year"] is not None:
            lines.append(f"该统计资料的截止年份：{card['through_year']}年，不能自动扩展到此后的年份。")
        for field in card["text_fields"]:
            lines.append(f"实际颁发年份：{field['value']}年；原文定位：{field['exact_quote']}。")
        for check in card["quoted_checks"]:
            status = "匹配资料主体别名" if check["matching_aliases"] else "未匹配该资料主体别名；不得把资料主体改名"
            lines.append(f"题设引号内容“{check['quoted_text']}”：{status}。")
    return "\n".join(lines)


class EvidenceBindingPolicy:
    def __init__(self, retriever, top_k=2, min_score=1.5):
        self.original = AntiHallucination(retriever, top_k, min_score)

    def prepare(self, question, policy="binding_cards", category=None):
        if policy not in POLICIES:
            raise ValueError("Unknown evidence binding policy")
        prepared = self.original.prepare(question, "combined", category)
        cards = [] if category in ("math_logic", "normal_control") else evidence_cards(question, prepared["evidence"])
        if policy == "binding_cards" and cards:
            prepared["prompt"] = render_cards(cards) + "\n\n" + prepared["prompt"]
        return {**prepared, "mode": policy, "reading_cards": cards,
                "reading_cards_applied": policy == "binding_cards" and bool(cards),
                "answer_override": None, "evaluation_status": "development_only"}
