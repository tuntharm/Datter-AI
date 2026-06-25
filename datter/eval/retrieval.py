from __future__ import annotations

import re

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def _tokenize(text: str) -> list[str]:
    return re.findall(r"\b\w+\b", text.lower())


def build_index(chunks_df: pd.DataFrame) -> tuple[TfidfVectorizer, pd.DataFrame]:
    texts = chunks_df["text"].fillna("").astype(str).tolist()
    vectorizer = TfidfVectorizer(max_features=8000, stop_words="english")
    if not texts:
        matrix = vectorizer.fit_transform([""])
    else:
        matrix = vectorizer.fit_transform(texts)
    return vectorizer, matrix


def retrieve_top_k(
    query: str,
    chunks_df: pd.DataFrame,
    vectorizer: TfidfVectorizer,
    matrix,
    k: int = 3,
    allowed_ids: set[str] | None = None,
) -> pd.DataFrame:
    if chunks_df.empty:
        return chunks_df

    subset = chunks_df
    if allowed_ids is not None:
        subset = chunks_df[chunks_df["item_id"].isin(allowed_ids)]
        if subset.empty:
            subset = chunks_df

    idx_map = {i: row.item_id for i, row in enumerate(subset.itertuples())}
    sub_texts = subset["text"].fillna("").astype(str).tolist()
    if not sub_texts:
        return subset.head(0)

    sub_matrix = vectorizer.transform(sub_texts)
    q_vec = vectorizer.transform([query])
    sims = cosine_similarity(q_vec, sub_matrix).flatten()
    order = sims.argsort()[::-1][:k]
    rows = [subset.iloc[i] for i in order if i < len(subset)]
    return pd.DataFrame(rows)


def gold_hint_recall(retrieved_df: pd.DataFrame, gold_hint: str, k: int = 3) -> float:
    if not gold_hint or retrieved_df.empty:
        return 0.0
    hint_tokens = set(_tokenize(gold_hint))
    if not hint_tokens:
        return 0.0
    hits = 0
    for _, row in retrieved_df.head(k).iterrows():
        text_tokens = set(_tokenize(str(row.get("text", ""))))
        overlap = len(hint_tokens & text_tokens) / len(hint_tokens)
        if overlap >= 0.3:
            hits += 1
    return hits / min(k, len(retrieved_df))
