"""Validate attributed reviews; AI developer checks never imply independent human evidence."""
from collections import Counter, defaultdict

from src.utils.experiment_io import stable_hash

LABELS = {
    "core_answer": {"correct", "incorrect", "partial", "not_answered", "unverifiable", "not_applicable"},
    "factual_error": {"present", "absent", "unverifiable", "not_applicable"},
    "unsupported_claims": {"yes", "no", "unclear"},
    "premise_handling": {"corrects", "accepts", "misses", "not_applicable", "unverifiable"},
    "refusal": {"none", "appropriate", "inappropriate", "unclear"},
    "response_type": {"substantive", "abstention_only", "mixed", "source_only", "empty"},
    "evidence_use": {"supported", "contradicted", "insufficient_evidence", "no_evidence", "not_applicable", "unresolved"},
}
CORE_COMPARABLE = {"correct", "incorrect", "partial", "not_answered"}


def fingerprint(record):
    return stable_hash({k: str(record.get(k, "")) for k in ("id", "mode", "question", "answer")})


def validate_review(review, record, valid_sources):
    if str(review["id"]) != str(record["id"]) or review["mode"] != record["mode"]:
        raise ValueError("Review identity mismatch")
    if review["content_sha256"] != fingerprint(record):
        raise ValueError("Review refers to a different question/answer")
    reviewer = review.get("reviewer_id")
    if review.get("reviewer_type") not in ("human", "ai_developer") or not isinstance(reviewer, str) or not reviewer.strip() or reviewer != reviewer.strip():
        raise ValueError("Explicit reviewer identity and type required")
    if not isinstance(review.get("rationale"), str) or not review["rationale"].strip():
        raise ValueError("A substantive review rationale is required")
    if "status" in record and record["status"] != "ok":
        raise ValueError("Only successfully generated or policy-answered records can be graded")
    for key, allowed in LABELS.items():
        if review.get(key) not in allowed:
            raise ValueError(f"Missing/invalid label: {key}")
    if record.get("data_role") == "uncertainty_probe" and review["core_answer"] in CORE_COMPARABLE:
        raise ValueError("Unestablished entity truth cannot receive a factual correctness label")
    sources = review.get("source_ids", [])
    if not isinstance(sources, list) or any(not isinstance(s, str) or not s.strip() for s in sources):
        raise ValueError("source_ids must be a list of nonempty registered IDs")
    if any(source not in valid_sources for source in sources):
        raise ValueError("Unregistered review evidence")
    if (review["core_answer"] in {"correct", "incorrect", "partial"} or review["factual_error"] == "present") and not sources:
        raise ValueError("Factual judgments require recorded evidence or derivation")
    if record.get("answer_origin") == "policy_abstention" and review["response_type"] != "abstention_only":
        raise ValueError("Do not mislabel a policy abstention as model-generated substantive content")


def agreement(reviews, label="core_answer"):
    if label not in LABELS:
        raise ValueError("Unknown agreement dimension")
    allowed = CORE_COMPARABLE if label == "core_answer" else LABELS[label]
    groups = defaultdict(list)
    for r in reviews:
        if r["reviewer_type"] == "human" and r.get(label) in allowed:
            groups[(r["run"], str(r["id"]), r["mode"], r["content_sha256"])].append(r)
    by_pair = defaultdict(list)
    for group in groups.values():
        identities = {r["reviewer_id"] for r in group}
        if len(identities) == 2 and len(group) == 2:
            by_pair[tuple(sorted(identities))].append(tuple(r[label] for r in sorted(group, key=lambda r: r["reviewer_id"])))
    if not by_pair:
        return {"status": "unavailable", "reason": "Requires two distinct human reviewers of identical records", "n": 0, "kappa": None}
    results = []
    for identities, pairs in sorted(by_pair.items()):
        n = len(pairs)
        observed = sum(a == b for a, b in pairs) / n
        a_counts, b_counts = Counter(a for a, b in pairs), Counter(b for a, b in pairs)
        expected = sum(a_counts[k] * b_counts[k] for k in allowed) / n ** 2
        results.append({"reviewers": identities, "n": n, "agreement_numerator": sum(a == b for a, b in pairs),
                        "agreement_denominator": n, "kappa": (observed - expected) / (1 - expected) if expected != 1 else None})
    if len(results) == 1:
        return {"status": "available", **results[0]}
    return {"status": "available_by_reviewer_pair", "n": sum(r["n"] for r in results), "kappa": None, "pairs": results}


def metric_tables(records):
    """One resolved label set per raw answer; attribution is handled by callers."""
    groups = defaultdict(list)
    seen = set()
    for r in records:
        key = (r["run"], str(r["id"]), r["mode"])
        if key in seen:
            raise ValueError("Do not count multiple opinions as multiple model answers")
        seen.add(key)
        groups[(r["run"], r["mode"])].append(r)
    tables = []
    for (run, mode), group in sorted(groups.items()):
        core = [r for r in group if r["core_answer"] in CORE_COMPARABLE]
        factual = [r for r in group if r["factual_error"] in ("present", "absent")]
        tables.append({"run": run, "mode": mode, "reviewed": len(group),
                       "core_correct_numerator": sum(r["core_answer"] == "correct" for r in core),
                       "core_correct_denominator": len(core),
                       "core_unverifiable_or_na": len(group) - len(core),
                       "factual_error_numerator": sum(r["factual_error"] == "present" for r in factual),
                       "factual_error_denominator": len(factual),
                       "factual_unverifiable_or_na": len(group) - len(factual),
                       "unsupported_claims": dict(Counter(r["unsupported_claims"] for r in group)),
                       "refusal": dict(Counter(r["refusal"] for r in group)),
                       "evidence_use": dict(Counter(r["evidence_use"] for r in group))})
    return tables


def summarize(reviews, include_ai=False):
    unique = set()
    for r in reviews:
        key = (r["run"], str(r["id"]), r["mode"], r["reviewer_id"])
        if key in unique:
            raise ValueError("Duplicate judgments from the same reviewer")
        unique.add(key)
    selected = [r for r in reviews if include_ai or r["reviewer_type"] == "human"]
    # Without adjudication, different human opinions must not be pooled into duplicated answers.
    by_record = defaultdict(list)
    for r in selected:
        by_record[(r["run"], str(r["id"]), r["mode"])].append(r)
    conflicts = [key for key, group in by_record.items() if len(group) > 1]
    tables = metric_tables(selected) if not conflicts else []
    return {"review_scope": "includes_ai_developer_not_independent_human" if include_ai else "human_only",
            "status": "adjudication_required" if conflicts else "ready" if selected else "no_independent_human_reviews",
            "review_count": len(selected), "unadjudicated_record_count": len(conflicts),
            "tables": tables, "human_agreement": agreement(reviews),
            "warning": "Purposefully selected development cases; no population-level effectiveness claim."}
