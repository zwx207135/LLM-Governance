"""Opt-in anchor disambiguation; frozen LocalRetriever behaviour is unchanged."""
import re

from src.governance.retrieval import LocalRetriever


def anchor_matches(topic, question):
    """Match an explicit topic, excluding documented lexical collisions.

    This is lexical filtering, not entity linking or proof of factual support.
    Mask Nobel only while matching Bell, so an explicit Bell elsewhere survives.
    """
    topic, question = topic.lower(), question.lower()
    if topic == "贝尔":
        question = question.replace("诺贝尔", "\ufffd" * 3)
    if re.fullmatch(r"[a-z0-9][a-z0-9 ._-]*", topic):
        return re.search(r"(?<![a-z0-9_])" + re.escape(topic) + r"(?![a-z0-9_])", question) is not None
    return topic in question


class SafeAnchorRetriever(LocalRetriever):
    def search_with_diagnostics(self, question, top_k=2, min_score=1.5):
        if top_k < 1:
            raise ValueError("top_k must be positive")
        # Filter before final truncation: otherwise a rejected hit can hide a
        # lower-scoring valid candidate. Preserve original BM25 scores/order.
        candidates = super().search(question, len(self.chunks), min_score)
        accepted, rejected = [], []
        for hit in candidates:
            anchors = [t for t in hit["topics"] if anchor_matches(t, question)]
            if anchors:
                accepted.append(hit)
            else:
                rejected.append({"chunk_id": hit["id"], "reason": "lexical_anchor_collision",
                                 "legacy_anchors": [t for t in hit["topics"] if t.lower() in question.lower()]})
        return {"hits": accepted[:top_k], "rejected": rejected}

    def search(self, question, top_k=2, min_score=1.5):
        return self.search_with_diagnostics(question, top_k, min_score)["hits"]
