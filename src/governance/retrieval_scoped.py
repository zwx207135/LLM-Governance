"""Opt-in metadata filtering for curated award records; not factual verification."""
import re

from src.governance.retrieval_safe import SafeAnchorRetriever, anchor_matches

CATEGORIES = {"physics": ("物理", "physics"), "literature": ("文学", "literature"),
              "chemistry": ("化学", "chemistry"), "peace": ("和平", "peace"),
              "medicine": ("医学", "生理", "medicine"), "economics": ("经济", "economic")}


class AwardScopedRetriever(SafeAnchorRetriever):
    annual_records_can_challenge_subject = False
    exclude_scientific_history_from_award_answers = False
    def search_with_diagnostics(self, question, top_k=2, min_score=1.5):
        if top_k < 1:
            raise ValueError("top_k must be positive")
        parent = super().search_with_diagnostics(question, len(self.chunks), min_score)
        lower = question.lower()
        if "诺贝尔" not in lower and "nobel" not in lower:
            return {**parent, "hits": parent["hits"][:top_k], "selection_events": []}
        categories = {key for key, aliases in CATEGORIES.items() if any(a in lower for a in aliases)}
        years = set(re.findall(r"(?<!\d)((?:19|20)\d{2})(?!\d)", question))
        # Multi-year comparisons must retain both years rather than picking one.
        year = int(next(iter(years))) if len(years) == 1 else None
        known_subjects = {a for c in self.chunks for a in c.get("scope", {}).get("subject_aliases", []) if anchor_matches(a, question)}
        quoted = re.findall(r"[“\"「]([^”\"」]+)[”\"」]", question)
        count_query = any(t in lower for t in ("几次", "多少次", "次数", "重复", "两次", "how many"))
        accepted, rejected = [], list(parent["rejected"])
        for hit in parent["hits"]:
            scope = hit.get("scope", {})
            kind = scope.get("kind")
            reason = None
            if scope.get("award_category") and categories and scope["award_category"] not in categories:
                reason = "award_category_mismatch"
            elif kind == "award_record":
                if year is not None and scope["award_year"] != year:
                    reason = "award_year_mismatch"
                elif known_subjects and not (year is not None and self.annual_records_can_challenge_subject) and not any(a in known_subjects for a in scope.get("subject_aliases", [])):
                    reason = "award_subject_mismatch"
                elif quoted and not (year is not None and self.annual_records_can_challenge_subject) and not any(a.lower() in phrase.lower() or phrase.lower() in a.lower()
                                        for phrase in quoted for a in scope.get("subject_aliases", [])):
                    reason = "quoted_subject_not_in_record"
            elif kind == "award_statistics" and (year is not None or not count_query):
                reason = "statistics_outside_query_scope"
            elif kind == "scientific_history" and (year is not None or self.exclude_scientific_history_from_award_answers):
                reason = "scientific_history_not_annual_award_record"
            if reason:
                rejected.append({"chunk_id": hit["id"], "reason": reason})
            else:
                accepted.append(hit)
        if self.exclude_scientific_history_from_award_answers and any(h.get("scope", {}).get("kind") == "award_record" for h in accepted):
            retained = []
            for hit in accepted:
                if hit.get("scope", {}).get("kind") in ("award_record", "award_statistics"):
                    retained.append(hit)
                else:
                    rejected.append({"chunk_id": hit["id"], "reason": "prefer_scoped_award_records_over_general_history"})
            accepted = retained
        selected = accepted[:top_k]
        events = []
        # A count needs both an individual record and the repeat-award scope.
        # This assembles evidence; it neither computes nor inserts an answer.
        if count_query and year is None and top_k >= 2 and known_subjects:
            records = [h for h in accepted if h.get("scope", {}).get("kind") == "award_record"]
            statistics = [h for h in accepted if h.get("scope", {}).get("kind") == "award_statistics"]
            if records and statistics:
                selected = [records[0], statistics[0]] + [h for h in accepted if h["id"] not in {records[0]["id"], statistics[0]["id"]}][:top_k - 2]
                events.append("paired_individual_record_with_repeat_award_statistics")
        return {"hits": selected, "rejected": rejected, "selection_events": events}


class AwardScopedRetrieverV2(AwardScopedRetriever):
    """Annual full recipient lists may refute a named premise; award records
    take precedence over general scientific history for award questions.
    V1 remains available to replay its documented failures.
    """
    annual_records_can_challenge_subject = True
    exclude_scientific_history_from_award_answers = True
