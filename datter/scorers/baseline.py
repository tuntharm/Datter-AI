from __future__ import annotations

import gzip
import re

import pandas as pd

from datter.scorers.base import SCORE_COLUMNS, BaseScorer

BOILERPLATE_PHRASES = (
    "all rights reserved",
    "lorem ipsum",
    "see appendix",
    "confidential",
    "terms and conditions",
    "no action required",
    "as discussed",
    "follow up",
)

STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "is", "are", "was", "were", "be", "been",
    "this", "that", "it", "as", "we", "you", "they", "i",
}


def gzip_complexity(text: str) -> float:
    raw = text.encode("utf-8")
    if not raw:
        return 0.0
    compressed = gzip.compress(raw)
    ratio = len(compressed) / len(raw)
    return BaseScorer.clamp(1.0 - ratio)


def type_token_ratio(text: str) -> float:
    tokens = re.findall(r"\b\w+\b", text.lower())
    if not tokens:
        return 0.0
    return len(set(tokens)) / len(tokens)


def stopword_ratio(text: str) -> float:
    tokens = re.findall(r"\b\w+\b", text.lower())
    if not tokens:
        return 1.0
    stops = sum(1 for t in tokens if t in STOPWORDS)
    return stops / len(tokens)


def boilerplate_penalty(text: str) -> float:
    lower = text.lower()
    hits = sum(1 for phrase in BOILERPLATE_PHRASES if phrase in lower)
    return min(0.4, hits * 0.1)


def recommend_action(usefulness: float, redundancy: float, density: float, row: pd.Series) -> tuple[str, str]:
    if row.get("is_exact_duplicate") and not row.get("is_canonical", True):
        return "drop", "Exact duplicate of another chunk; canonical copy retained elsewhere."
    if redundancy >= 0.92 and usefulness < 0.35:
        return "drop", "Highly redundant with low usefulness."
    if redundancy >= 0.92:
        return "drop", "Near-verbatim overlap with existing corpus content."
    if usefulness >= 0.55 and redundancy < 0.75:
        return "keep", "High usefulness with acceptable redundancy."
    if redundancy >= 0.75:
        return "compress", "Substantial overlap; summarize or deduplicate before indexing."
    if density < 0.25:
        return "drop", "Low information density — likely boilerplate or filler."
    if 0.30 <= usefulness < 0.55:
        return "review", "Borderline usefulness; human review recommended."
    return "review", "Mixed signals; inspect before committing AI spend."


class BaselineScorer(BaseScorer):
    name = "baseline"

    def fit(self, data: pd.DataFrame) -> BaselineScorer:
        return self

    def score(self, items: pd.DataFrame) -> pd.DataFrame:
        if items.empty:
            return self.empty_scores(items)

        rows = []
        for _, row in items.iterrows():
            text = str(row.get("text", ""))
            redundancy = BaseScorer.clamp(float(row.get("max_similarity", 0.0)))
            if row.get("is_exact_duplicate") and not row.get("is_canonical", True):
                redundancy = 1.0
            elif row.get("is_exact_duplicate"):
                redundancy = max(redundancy, 0.95)

            ttr = type_token_ratio(text)
            novelty = BaseScorer.clamp(1.0 - redundancy + 0.15 * ttr)
            sw = stopword_ratio(text)
            length_score = BaseScorer.clamp(len(text) / 800)
            density = BaseScorer.clamp(
                0.45 * ttr + 0.35 * (1.0 - sw) + 0.20 * length_score - boilerplate_penalty(text)
            )
            complexity = gzip_complexity(text)
            usefulness = BaseScorer.clamp(0.4 * novelty + 0.35 * density - 0.25 * redundancy)

            action, explanation = recommend_action(usefulness, redundancy, density, row)
            rows.append(
                {
                    "item_id": row["item_id"],
                    "complexity_score": round(complexity, 4),
                    "usefulness_score": round(usefulness, 4),
                    "redundancy_score": round(redundancy, 4),
                    "novelty_score": round(novelty, 4),
                    "information_density_score": round(density, 4),
                    "recommended_action": action,
                    "explanation": explanation,
                }
            )

        return pd.DataFrame(rows, columns=SCORE_COLUMNS)
