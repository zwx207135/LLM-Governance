"""Exploratory final-question decomposition for unmatched quoted award subjects."""
import re

from src.governance.anti_hallucination import AntiHallucination
from src.governance.retrieval_safe import anchor_matches

POLICIES = ("combined", "subject_focus")


class SubjectFocusPolicy:
    def __init__(self, retriever, top_k=2, min_score=1.5):
        self.original = AntiHallucination(retriever, top_k, min_score)

    def prepare(self, question, policy="subject_focus", category=None):
        if policy not in POLICIES:
            raise ValueError("Unknown subject focus policy")
        result = self.original.prepare(question, "combined", category)
        quoted = re.findall(r'[“「『"]([^”」』"]{1,80})[”」』"]', question)
        records = [h for h in result["evidence"] if h.get("scope", {}).get("kind") == "award_record"]
        aliases = [a for h in records for a in h["scope"].get("subject_aliases", [])]
        missing = [name for name in quoted if not any(anchor_matches(a, name) for a in aliases)]
        applied = policy == "subject_focus" and bool(records and missing) and category not in ("math_logic", "normal_control")
        if applied:
            labels = "、".join("[" + h["id"] + "]" for h in records)
            result["prompt"] += (f"\n\n请按两步回答原问题：第一步，只按资料{labels}列出该年度实际记载的获奖者。"
                                 f"第二步，核对原问题中的“{'、'.join(missing)}”是否有明确获奖身份证据。"
                                 "若资料未建立该身份，应说明无法据这些资料介绍该姓名的获奖贡献或作品；不得把资料人物改名。"
                                 "不要仅输出资料编号或链接。")
        return {**result, "mode": policy, "subject_focus_applied": applied,
                "focus_record_ids": [h["id"] for h in records], "unmatched_quoted_text": missing,
                "answer_override": None, "evaluation_status": "C_developer_diagnostic_only"}
