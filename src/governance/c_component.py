"""C-only explicit handoff profile; existing global service defaults stay intact."""
import hashlib
import json
import math
from pathlib import Path

from src.governance.retrieval import LocalRetriever
from src.governance.retrieval_safe import SafeAnchorRetriever
from src.governance.retrieval_year_alias import AwardYearAliasRetriever
from src.governance.service import GovernanceService, STRATEGIES

FIELDS = {"schema_version", "stage", "corpus", "corpus_sha256", "retriever", "top_k", "min_score", "strategy"}


def load_profile(root, profile_path=None):
    root = Path(root).resolve()
    path = Path(profile_path) if profile_path else root / "configs/c_component_profile.json"
    config = json.loads(path.read_text(encoding="utf-8"))
    if set(config) != FIELDS or config["schema_version"] != 1:
        raise ValueError("Unknown or missing C profile fields; no reference/gold inputs accepted")
    if config["retriever"] not in ("legacy", "safe_anchor", "year_alias") or config["strategy"] not in STRATEGIES:
        raise ValueError("Unknown C implementation or strategy")
    if type(config["top_k"]) is not int or config["top_k"] < 1:
        raise ValueError("Positive integer top_k required")
    if type(config["min_score"]) not in (int, float) or not math.isfinite(config["min_score"]) or config["min_score"] < 0:
        raise ValueError("Finite nonnegative min_score required")
    corpus = (root / config["corpus"]).resolve()
    if not corpus.is_relative_to(root):
        raise ValueError("Corpus must be inside the explicit project root")
    if hashlib.sha256(corpus.read_bytes()).hexdigest() != config["corpus_sha256"]:
        raise ValueError("C profile corpus hash differs; create a new explicit profile")
    return config, corpus


def build_c_service(root, model_factory, profile_path=None):
    config, corpus = load_profile(root, profile_path)
    implementations = {"legacy": LocalRetriever, "safe_anchor": SafeAnchorRetriever, "year_alias": AwardYearAliasRetriever}
    retriever = implementations[config["retriever"]](corpus)
    service = GovernanceService(retriever, model_factory, top_k=config["top_k"], min_score=config["min_score"])
    return service, retriever, config
