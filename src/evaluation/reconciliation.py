"""Resolve genuinely attributed human reviews without manufacturing additional reviewers."""
from collections import defaultdict

from src.evaluation.review_metrics import LABELS, agreement, metric_tables, validate_review
from src.utils.experiment_io import stable_hash


def identity(row):
    return row["run"], str(row["id"]), row["mode"]


def review_groups(reviews):
    groups, seen = defaultdict(list), set()
    for review in reviews:
        key = (*identity(review), review["reviewer_id"])
        if key in seen:
            raise ValueError("Duplicate reviewer judgments; preserve revisions in separate input versions")
        seen.add(key)
        if review["reviewer_type"] == "human":
            groups[identity(review)].append(review)
    result = []
    for key, group in sorted(groups.items()):
        if len({r["content_sha256"] for r in group}) != 1:
            raise ValueError("Human reviews refer to different raw answers")
        if len(group) > 2:
            raise ValueError("This protocol requires exactly two independent reviewers per answer")
        group = sorted(group, key=lambda r: r["reviewer_id"])
        disagreements = [label for label in LABELS if len({r[label] for r in group}) > 1]
        result.append({"resolution_id": "J" + stable_hash(list(key))[:20], "run": key[0], "id": key[1], "mode": key[2],
                       "content_sha256": group[0]["content_sha256"], "review_group_sha256": stable_hash(group),
                       "reviewer_ids": [r["reviewer_id"] for r in group], "original_reviews": group,
                       "state": "single_review" if len(group) == 1 else "conflict" if disagreements else "consensus",
                       "disagreement_dimensions": disagreements})
    return result


def reconcile(reviews, decisions=None, adjudicator_id=None, records=None, valid_sources=None):
    groups = review_groups(reviews)
    conflicts = {g["resolution_id"]: g for g in groups if g["state"] == "conflict"}
    supplied = {}
    for decision in decisions or []:
        if not any(str(decision.get(k, "")).strip() for k in [*LABELS, "source_ids", "rationale"]):
            continue
        if not isinstance(adjudicator_id, str) or not adjudicator_id.strip():
            raise ValueError("An explicit human adjudicator identity is required")
        ident = decision["resolution_id"]
        if ident not in conflicts or ident in supplied:
            raise ValueError("Unknown, non-conflicting or duplicate adjudication identity")
        group = conflicts[ident]
        if decision.get("review_group_sha256") != group["review_group_sha256"]:
            raise ValueError("Original reviews changed since this adjudication form was created")
        sources = decision.get("source_ids", [])
        if isinstance(sources, str):
            sources = [s.strip() for s in sources.split(";") if s.strip()]
        review = {k: group[k] for k in ("run", "id", "mode", "content_sha256")}
        review.update({k: str(decision.get(k, "")).strip() for k in LABELS})
        review.update(reviewer_id=adjudicator_id.strip(), reviewer_type="human", source_ids=sources,
                      rationale=str(decision.get("rationale", "")).strip())
        if records is None or valid_sources is None:
            raise ValueError("Adjudication requires raw answer validation and registered evidence")
        validate_review(review, records[identity(review)], valid_sources)
        supplied[ident] = review
    resolved = []
    for group in groups:
        if group["state"] == "single_review" or (group["state"] == "conflict" and group["resolution_id"] not in supplied):
            continue
        result = {k: group[k] for k in ("resolution_id", "run", "id", "mode", "content_sha256", "review_group_sha256", "reviewer_ids")}
        if group["state"] == "consensus":
            originals = group["original_reviews"]
            result.update({k: originals[0][k] for k in LABELS})
            result.update(resolution_origin="two_human_consensus", source_ids=sorted({s for r in originals for s in r["source_ids"]}),
                          original_rationales={r["reviewer_id"]: r["rationale"] for r in originals})
        else:
            decision = supplied[group["resolution_id"]]
            result.update({k: decision[k] for k in [*LABELS, "source_ids", "rationale"]})
            result.update(resolution_origin="explicit_human_adjudication", adjudicator_id=decision["reviewer_id"])
        resolved.append(result)
    pending_conflicts = len(conflicts) - len(supplied)
    single = sum(g["state"] == "single_review" for g in groups)
    humans = sum(r["reviewer_type"] == "human" for r in reviews)
    report = {"protocol": "c-two-human-resolution-v1", "scope": "human_only_resolved_answers",
              "status": "no_independent_human_reviews" if not humans else "pending_independent_review" if single or pending_conflicts else "resolved_reviewed_subset",
              "human_judgment_records": humans, "ai_judgments_excluded": len(reviews) - humans,
              "unique_human_reviewed_answers": len(groups), "consensus_answers": sum(g["state"] == "consensus" for g in groups),
              "adjudicated_answers": len(supplied), "single_review_answers": single,
              "unresolved_conflict_answers": pending_conflicts, "resolved_answers": len(resolved),
              "resolved_fraction_of_human_reviewed_answers": len(resolved) / len(groups) if groups else None,
              "agreement_before_adjudication": {label: agreement(reviews, label) for label in LABELS},
              "tables": metric_tables(resolved),
              "warning": "Tables describe only resolved reviewed answers; no population-level effectiveness or full test completion claim."}
    return {"report": report, "resolved_records": resolved, "review_groups": groups}
