from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

from datter.eval.queries import load_queries

STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "is", "are", "was", "were", "be", "been",
    "this", "that", "it", "as", "we", "you", "they", "what", "how", "who",
}


def _tokenize(text: str) -> set[str]:
    return {t for t in re.findall(r"\b\w+\b", text.lower()) if len(t) > 2 and t not in STOPWORDS}


def build_term_weights(queries_path: Path) -> dict[str, float]:
    """Weight eval query + gold_hint tokens; gold hints count double."""
    config = load_queries(queries_path)
    weights: dict[str, float] = {}
    for q in config.questions:
        for token in _tokenize(q.query):
            weights[token] = weights.get(token, 0.0) + 1.0
        for token in _tokenize(q.gold_hint):
            weights[token] = weights.get(token, 0.0) + 3.0
    return weights


def chunk_relevance_score(text: str, term_weights: dict[str, float]) -> float:
    if not term_weights or not text:
        return 0.0
    text_tokens = _tokenize(text)
    if not text_tokens:
        return 0.0
    total_weight = sum(term_weights.values())
    if total_weight <= 0:
        return 0.0
    hit_weight = sum(term_weights[t] for t in text_tokens if t in term_weights)
    return min(1.0, hit_weight / total_weight * 3.0)


def apply_query_relevance_boost(
    scores: pd.DataFrame,
    items_df: pd.DataFrame,
    queries_path: Path,
    boost_weight: float = 0.55,
) -> pd.DataFrame:
    """Blend task/query relevance into usefulness for selection ranking."""
    if scores.empty or not queries_path.is_file():
        return scores

    term_weights = build_term_weights(queries_path)
    if not term_weights:
        return scores

    text_by_id = dict(zip(items_df["item_id"], items_df["text"].fillna("").astype(str)))
    boosted = scores.copy()
    for idx, row in boosted.iterrows():
        rel = chunk_relevance_score(text_by_id.get(row["item_id"], ""), term_weights)
        base = float(row["usefulness_score"])
        boosted.at[idx, "usefulness_score"] = round(min(1.0, base + boost_weight * rel), 4)
    return boosted
