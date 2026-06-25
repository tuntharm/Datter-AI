from __future__ import annotations

import re

import pandas as pd


def _best_sentences(text: str, query: str, max_sentences: int = 3) -> str:
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    if not sentences:
        return text[:400]
    query_tokens = set(re.findall(r"\b\w+\b", query.lower()))
    scored = []
    for s in sentences:
        s_tokens = set(re.findall(r"\b\w+\b", s.lower()))
        overlap = len(query_tokens & s_tokens)
        scored.append((overlap, s))
    scored.sort(key=lambda x: x[0], reverse=True)
    picked = [s for _, s in scored[:max_sentences] if s.strip()]
    return " ".join(picked) if picked else text[:400]


def synthesize_answer(query: str, retrieved_df: pd.DataFrame) -> str:
    if retrieved_df.empty:
        return "No relevant context found in corpus."
    parts = []
    for _, row in retrieved_df.iterrows():
        snippet = _best_sentences(str(row.get("text", "")), query)
        if snippet:
            parts.append(snippet)
    combined = " ".join(parts)
    return combined[:1200] if combined else "No relevant context found in corpus."


def answer_from_corpus(
    query: str,
    chunks_df: pd.DataFrame,
    vectorizer,
    matrix,
    allowed_ids: set[str] | None,
    retrieval_fn,
) -> str:
    retrieved = retrieval_fn(query, chunks_df, vectorizer, matrix, allowed_ids=allowed_ids)
    return synthesize_answer(query, retrieved)
