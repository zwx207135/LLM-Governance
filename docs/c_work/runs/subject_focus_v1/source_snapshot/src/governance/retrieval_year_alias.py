"""Metadata-guided year alias fallback; frozen V2 remains unchanged."""
import re

from src.governance.retrieval_scoped import AwardScopedRetrieverV2, CATEGORIES


class AwardYearAliasRetriever(AwardScopedRetrieverV2):
    def search_with_diagnostics(self, question, top_k=2, min_score=1.5):
        result = super().search_with_diagnostics(question, top_k, min_score)
        result["query_expansion"] = None
        lower = question.lower()
        if result["hits"] or not ("诺贝尔" in question or "nobel" in lower):
            return result
        years = set(re.findall(r"(?<!\d)((?:19|20)\d{2})(?!\d)", question))
        categories = {k for k, aliases in CATEGORIES.items() if any(a in lower for a in aliases)}
        # Only a unique explicit year and category can admit this fallback.
        # Never supply another year's record for an uncovered year.
        if len(years) != 1 or len(categories) != 1:
            return result
        year, category = int(next(iter(years))), next(iter(categories))
        candidates = [c for c in self.chunks if c.get("scope", {}).get("kind") == "award_record"
                      and c["scope"]["award_year"] == year and c["scope"]["award_category"] == category]
        if not candidates:
            return result
        # Use source-derived aliases to admit and score the already matching
        # records. Log the effective query; no answer/reference input exists.
        aliases = list(dict.fromkeys(c["topics"][0] for c in candidates))
        expanded = question + "\n检索主题别名：" + "、".join(aliases)
        fallback = super().search_with_diagnostics(expanded, len(self.chunks), min_score)
        allowed = {c["id"] for c in candidates}
        hits = [h for h in fallback["hits"] if h["id"] in allowed][:top_k]
        return {**result, "hits": hits,
                "selection_events": result.get("selection_events", []) + (["explicit_year_category_alias_fallback"] if hits else []),
                "query_expansion": {"effective_query": expanded, "added_aliases": aliases, "eligible_chunk_ids": sorted(allowed),
                                    "scoring_query": "expanded", "fallback_rejected": fallback["rejected"]}}
