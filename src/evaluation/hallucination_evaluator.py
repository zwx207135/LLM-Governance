"""可解释的幻觉评估基线。

评分范围为 [0, 1]：
- factual_score 越高，回答与参考答案的关键词重合越多。
- logical_score 越高，回答中检测到的显式矛盾越少。
- hallucination_score 越高，基线规则判定的幻觉风险越高。

这是基于规则的基线，不替代人工核验或专业事实判定模型。
"""

from __future__ import annotations

import re
from collections.abc import Iterable
from typing import Any


_DEFAULT_STOPWORDS = {
    "的", "了", "是", "在", "和", "与", "及", "或", "一个", "一种",
    "这个", "那个", "这些", "那些", "请", "介绍", "说明", "回答",
    "根据", "资料", "显示", "认为", "可以", "可能", "其中", "其",
    "为", "有", "对", "将", "把", "被", "并", "而", "但", "如果",
    "因为", "所以", "the", "a", "an", "is", "are", "was", "were",
    "of", "to", "in", "and", "or", "that", "this", "it",
}


def _tokens(text: str, stopwords: set[str]) -> set[str]:
    """抽取中英文关键词、数字和日期；中文用字符片段近似分词。"""
    text = text.lower()
    words = re.findall(r"[a-z]+(?:'[a-z]+)?|\d+(?:[.,]\d+)*", text)
    chinese_runs = re.findall(r"[\u4e00-\u9fff]+", text)

    for run in chinese_runs:
        words.extend(run)
        words.extend(run[i:i + 2] for i in range(len(run) - 1))
        words.extend(run[i:i + 3] for i in range(len(run) - 2))

    return {
        word for word in words
        if word not in stopwords and word.strip()
    }


class HallucinationEvaluator:
    """使用参考答案关键词覆盖率和显式矛盾规则评估回答。"""

    def __init__(
        self,
        factual_weight: float = 0.7,
        stopwords: Iterable[str] | None = None,
    ) -> None:
        if not 0 <= factual_weight <= 1:
            raise ValueError("factual_weight 必须在 0 到 1 之间")

        self.factual_weight = factual_weight
        self.stopwords = set(stopwords or _DEFAULT_STOPWORDS)

    def evaluate(
        self,
        question: str,
        answer: str,
        reference: str | dict[str, Any] | list[str],
    ) -> dict[str, Any]:
        """评估单条回答并返回分数与诊断信息。

        reference 可以是字符串、字符串列表，或包含 answer/claims 字段的字典。
        """
        if not isinstance(question, str):
            raise TypeError("question 必须是字符串")
        if not isinstance(answer, str):
            raise TypeError("answer 必须是字符串")

        reference_text = self._references(reference)
        if not reference_text.strip():
            raise ValueError(
                "reference 不能为空；没有参考答案时不能计算事实一致性"
            )

        answer_tokens = _tokens(answer, self.stopwords)
        reference_tokens = _tokens(reference_text, self.stopwords)

        if not answer.strip() or not reference_tokens:
            factual_score = 0.0
            matched_tokens: set[str] = set()
            missing_tokens = reference_tokens
        else:
            matched_tokens = answer_tokens & reference_tokens
            factual_score = len(matched_tokens) / len(reference_tokens)
            missing_tokens = reference_tokens - answer_tokens

        contradictions = self._find_contradictions(answer)
        logical_score = 0.0 if contradictions else 1.0

        hallucination_score = (
            self.factual_weight * (1.0 - factual_score)
            + (1.0 - self.factual_weight) * (1.0 - logical_score)
        )

        return {
            "factual_score": round(factual_score, 4),
            "logical_score": round(logical_score, 4),
            "hallucination_score": round(hallucination_score, 4),
            "details": {
                "matched_reference_terms": sorted(matched_tokens),
                "missing_reference_terms": sorted(missing_tokens),
                "contradictions": contradictions,
                "method": "keyword_coverage_and_explicit_contradiction_rules",
                "note": (
                    "规则基线分数仅供筛查，需结合人工或更强语义评估复核。"
                ),
            },
        }

    @staticmethod
    def _references(
        reference: str | dict[str, Any] | list[str],
    ) -> str:
        if isinstance(reference, str):
            return reference

        if isinstance(reference, list):
            if not all(isinstance(item, str) for item in reference):
                raise TypeError("reference 列表中的元素必须都是字符串")
            return " ".join(reference)

        if isinstance(reference, dict):
            value = reference.get("answer", reference.get("claims", ""))
            if isinstance(value, list):
                return " ".join(str(item) for item in value)
            return str(value)

        raise TypeError(
            "reference 必须是字符串、字符串列表或字典"
        )

    @staticmethod
    def _find_contradictions(answer: str) -> list[str]:
        """检测少量明确的自相矛盾模式，不尝试判断复杂推理。"""
        found: list[str] = []

        # 比较关系双向出现，例如“A比B高，B比A高”。
        comparison_patterns = (
            r"([^，。；\n]{1,20})比([^，。；\n]{1,20})(高|大|多|晚)",
            r"([^，。；\n]{1,20})比([^，。；\n]{1,20})(低|小|少|早)",
        )

        for pattern in comparison_patterns:
            relations = re.findall(pattern, answer)
            relation_set = {
                (left.strip(), right.strip(), relation)
                for left, right, relation in relations
            }

            for left, right, relation in relation_set:
                if left != right and (right, left, relation) in relation_set:
                    found.append(
                        f"比较关系方向矛盾：{left}与{right}的“{relation}”关系"
                    )
                    break

        # 显式“既是……又不是……”表达。
        if re.search(r"既是.{0,30}又不是", answer):
            found.append("检测到“既是……又不是……”的显式矛盾表达")

        return found