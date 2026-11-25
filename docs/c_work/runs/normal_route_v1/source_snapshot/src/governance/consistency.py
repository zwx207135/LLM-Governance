"""Deterministic consistency signals, not semantic entailment or factual scoring."""
import json
import re


def check_consistency(answer, evidence=(), evidence_labels=None, materials=()):
    if not isinstance(answer, str):
        raise ValueError("Actual answer text required")
    flags = []
    def flag(code, detail, certainty="mechanical"):
        flags.append({"code": code, "detail": detail, "kind": certainty})
    ids = {str(h["id"]) for h in evidence} | {str(m["id"]) for m in materials}
    labels = dict(evidence_labels or {})
    if not labels:
        labels = {i: i for i in ids}
    for material in materials:
        labels.setdefault(str(material["id"]), str(material["id"]))
    for label, target in labels.items():
        if str(target) not in ids:
            flag("invalid_evidence_mapping", str(label))
    cited = set(re.findall(r"\[([A-Za-z0-9][A-Za-z0-9_-]{0,63})\]", answer))
    for label in sorted(cited):
        if label not in labels or str(labels[label]) not in ids:
            flag("unknown_citation", label)
    urls = set(re.findall(r"https?://[^\s<>\]\)\u3002\uff0c]+", answer))
    known_urls = {h.get("source", {}).get("url") for h in evidence}
    for url in sorted(urls - known_urls):
        flag("url_not_in_supplied_evidence", url, "screening")
    parsed = None
    text = answer.strip()
    match = re.fullmatch(r"```(?:json)?\s*(.*?)\s*```", text, re.S | re.I)
    try:
        def pairs(items):
            out = {}
            for key, value in items:
                if key in out:
                    raise ValueError("duplicate key")
                out[key] = value
            return out
        parsed = json.loads(match.group(1) if match else text, object_pairs_hook=pairs)
    except ValueError:
        if text.startswith(("{", "```json")):
            flag("unparseable_structured_answer", "Cannot check structured fields")
    if isinstance(parsed, dict) and "verdict" in parsed and "basis" in parsed:
        verdict, basis = parsed["verdict"], parsed["basis"]
        if verdict in ("not_established", "不足") and basis != "none":
            flag("insufficient_with_selected_basis", str(basis))
        if verdict in ("supported", "refuted", "支持", "反驳") and basis == "none":
            flag("determinate_without_basis", str(verdict))
        available = {m["id"] for m in materials}
        if materials and basis != "none" and (not isinstance(basis, str) or basis not in available):
            flag("basis_outside_supplied_materials", str(basis))
    if re.search(r"无法核实|资料不足|无法确认", answer) and re.search(r"(?:售价|价格|续航|成立于|建成于).{0,12}\d", answer):
        flag("uncertainty_with_numeric_claim", "Review whether the number is asserted, quoted or hypothetical", "screening")
    return {"scope": "mechanical_consistency_and_screening_only", "flags": flags,
            "semantic_support": "not_evaluated", "factual_accuracy": None}
