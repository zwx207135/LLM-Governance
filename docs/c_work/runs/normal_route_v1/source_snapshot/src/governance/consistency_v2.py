"""Versioned structural audit; exact quote matching is not semantic entailment."""
import json
import re
from src.governance.consistency import check_consistency


def validate_materials(materials):
    if not isinstance(materials, (list, tuple)):
        raise ValueError("Materials must be an ordered list")
    seen = set()
    for m in materials:
        if not isinstance(m, dict) or set(m) - {"id", "text"} or not re.fullmatch(r"M[1-9][0-9]*", str(m.get("id", ""))):
            raise ValueError("Materials accept only M-number IDs and text")
        if m["id"] in seen or not isinstance(m.get("text"), str) or not m["text"].strip():
            raise ValueError("Distinct material IDs and nonempty text required")
        seen.add(m["id"])


def check_consistency_v2(answer, evidence=(), evidence_labels=None, materials=()):
    validate_materials(materials)
    result = check_consistency(answer, evidence, evidence_labels, materials)
    result["version"] = "consistency-v2"
    result["quote_support"] = "not_evaluated"
    text = answer.strip()
    match = re.fullmatch(r"```(?:json)?\s*(.*?)\s*```", text, re.S | re.I)
    def reject(value):
        raise ValueError("Nonfinite JSON")
    def unique_pairs(pairs):
        out = {}
        for key, value in pairs:
            if key in out:
                raise ValueError("Duplicate JSON key")
            out[key] = value
        return out
    try:
        parsed = json.loads(match.group(1) if match else text, parse_constant=reject, object_pairs_hook=unique_pairs)
    except ValueError:
        if re.search(r"\b(?:NaN|Infinity)\b", text):
            result["flags"].append({"code": "nonfinite_json_constant", "kind": "mechanical", "detail": "Not valid JSON"})
        return result
    if not isinstance(parsed, dict):
        return result
    for key, values in (("verdict", ("supported", "refuted", "not_established", "支持", "反驳", "不足")),):
        if key in parsed and (not isinstance(parsed[key], str) or parsed[key] not in values):
            result["flags"].append({"code": "invalid_verdict_value", "kind": "mechanical", "detail": key})
    if "quote" in parsed:
        quote, basis = parsed["quote"], parsed.get("basis")
        indexed = {m["id"]: m["text"] for m in materials}
        if isinstance(quote, str) and quote.strip() and isinstance(basis, str) and basis in indexed:
            matched = quote in indexed[basis]
            result["quote_support"] = "exact_substring_present" if matched else "exact_substring_absent"
            if not matched:
                result["flags"].append({"code": "quote_not_in_selected_material", "kind": "mechanical", "detail": basis})
        else:
            result["flags"].append({"code": "quote_not_checkable", "kind": "mechanical", "detail": "Nonempty quote and known material basis required"})
    return result
