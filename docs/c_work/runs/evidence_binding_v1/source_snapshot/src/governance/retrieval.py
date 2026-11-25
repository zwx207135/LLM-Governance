"""Dependency-free, deterministic Chinese BM25 over a versioned corpus."""
import hashlib
import json
import math
import re
from collections import Counter
from pathlib import Path


def tokens(text):
    text = re.sub(r"请介绍一下|请介绍|请说明|是什么|是多少|哪个|哪些|为什么|那么|是否|目前|现任|既然", " ", text.lower())
    result = re.findall(r"[a-z0-9]+", text)
    for word in re.findall(r"[\u4e00-\u9fff]+", text):
        result.extend(word[i:i + 2] for i in range(len(word) - 1))
    return result


class LocalRetriever:
    def __init__(self, corpus_path):
        raw = Path(corpus_path).read_bytes()
        self.sha256 = hashlib.sha256(raw).hexdigest()
        corpus = json.loads(raw)
        self.version = corpus["version"]
        self.sources = {s["id"]: s for s in corpus["sources"]}
        self.chunks = corpus["chunks"]
        ids = [c["id"] for c in self.chunks]
        if not ids or len(ids) != len(set(ids)):
            raise ValueError("Nonempty unique chunk IDs required")
        for c in self.chunks:
            source = self.sources[c["source_id"]]
            if not source.get("url") or not source.get("accessed_at"):
                raise ValueError("Source URL and access date required")
            if not c.get("topics") or not all(isinstance(t, str) and t.strip() for t in c["topics"]):
                raise ValueError("Explicit topic anchors required for every chunk")
        self.counts = [Counter(tokens(c["text"])) for c in self.chunks]
        self.lengths = [sum(c.values()) for c in self.counts]
        self.average = sum(self.lengths) / len(self.lengths)
        self.df = Counter(t for c in self.counts for t in c)

    def search(self, question, top_k=2, min_score=1.5):
        if top_k < 1:
            raise ValueError("top_k must be positive")
        query = set(tokens(question))
        hits = []
        for chunk, counts, length in zip(self.chunks, self.counts, self.lengths):
            # A common word such as 贡献/研究/最大 cannot establish subject relevance.
            if not any(topic.lower() in question.lower() for topic in chunk["topics"]):
                continue
            score = 0.0
            matched = sorted(query.intersection(counts))
            for term in matched:
                freq = counts[term]
                idf = math.log(1 + (len(self.chunks) - self.df[term] + .5) / (self.df[term] + .5))
                score += idf * freq * 2.5 / (freq + 1.5 * (.25 + .75 * length / self.average))
            if matched and score >= min_score:
                hits.append({**chunk, "score": round(score, 6), "matched_terms": matched,
                             "source": self.sources[chunk["source_id"]]})
        return sorted(hits, key=lambda h: (-h["score"], h["id"]))[:top_k]
