from __future__ import annotations

import random
from pathlib import Path

import pandas as pd

from datter.eval.relevance_boost import apply_query_relevance_boost
from datter.models import Chunk, SelectedCorpus


def _chunk_lookup(chunks: list[Chunk]) -> dict[str, Chunk]:
    return {c.item_id: c for c in chunks}


def _effective_tokens(action: str, token_count: int) -> int:
    if action == "drop":
        return 0
    if action == "compress":
        return max(1, token_count // 2)
    return token_count


def _selection_scores(
    chunks: list[Chunk],
    scores: pd.DataFrame,
    queries_path: Path | None,
    items_df: pd.DataFrame | None,
) -> pd.DataFrame:
    if queries_path and queries_path.is_file():
        if items_df is None:
            items_df = pd.DataFrame(
                [{"item_id": c.item_id, "text": c.text} for c in chunks]
            )
        return apply_query_relevance_boost(scores, items_df, queries_path)
    return scores


def select_datter_cut(
    chunks: list[Chunk],
    scores: pd.DataFrame,
    target_reduction: float = 0.50,
    queries_path: Path | None = None,
    items_df: pd.DataFrame | None = None,
) -> list[str]:
    if not chunks or scores.empty:
        return [c.item_id for c in chunks]

    working = _selection_scores(chunks, scores, queries_path, items_df)
    merged = working.set_index("item_id")
    target_keep = max(1, int(sum(c.token_count for c in chunks) * (1.0 - target_reduction)))

    ranked = []
    for chunk in chunks:
        row = merged.loc[chunk.item_id] if chunk.item_id in merged.index else None
        action = str(row["recommended_action"]) if row is not None else "review"
        usefulness = float(row["usefulness_score"]) if row is not None else 0.0
        if action == "drop":
            continue
        ranked.append((usefulness, action, chunk))

    ranked.sort(key=lambda x: x[0], reverse=True)

    kept: list[str] = []
    tokens = 0
    for _, action, chunk in ranked:
        eff = _effective_tokens(action, chunk.token_count)
        if tokens + eff > target_keep and kept:
            continue
        kept.append(chunk.item_id)
        tokens += eff
        if tokens >= target_keep:
            break

    if not kept and ranked:
        kept = [ranked[0][2].item_id]

    return kept


def select_random_cut(
    chunks: list[Chunk],
    scores: pd.DataFrame,
    datter_chunk_ids: list[str],
    seed: int = 42,
) -> list[str]:
    lookup = _chunk_lookup(chunks)
    idx = scores.set_index("item_id")
    datter_tokens = sum(
        _effective_tokens(
            str(idx.loc[cid, "recommended_action"]) if cid in idx.index else "keep",
            lookup[cid].token_count,
        )
        for cid in datter_chunk_ids
        if cid in lookup
    )

    eligible = [c for c in chunks if not c.is_exact_duplicate or c.is_canonical]
    if not eligible:
        eligible = list(chunks)

    rng = random.Random(seed)
    shuffled = eligible.copy()
    rng.shuffle(shuffled)

    kept: list[str] = []
    tokens = 0
    for chunk in shuffled:
        row = scores[scores["item_id"] == chunk.item_id]
        action = str(row.iloc[0]["recommended_action"]) if not row.empty else "keep"
        if action == "drop":
            continue
        eff = _effective_tokens(action, chunk.token_count)
        if tokens + eff > datter_tokens and kept:
            continue
        kept.append(chunk.item_id)
        tokens += eff
        if tokens >= datter_tokens:
            break

    if not kept and shuffled:
        kept = [shuffled[0].item_id]

    return kept


def build_selection(
    chunks: list[Chunk],
    scores: pd.DataFrame,
    target_reduction: float = 0.50,
    seed: int = 42,
    queries_path: Path | None = None,
    items_df: pd.DataFrame | None = None,
) -> SelectedCorpus:
    full_tokens = sum(c.token_count for c in chunks)
    datter_ids = select_datter_cut(
        chunks, scores, target_reduction, queries_path=queries_path, items_df=items_df
    )
    random_ids = select_random_cut(chunks, scores, datter_ids, seed=seed)
    lookup = _chunk_lookup(chunks)
    idx = scores.set_index("item_id")

    def _sum_tokens(ids: list[str]) -> int:
        total = 0
        for cid in ids:
            if cid not in lookup:
                continue
            action = str(idx.loc[cid, "recommended_action"]) if cid in idx.index else "keep"
            total += _effective_tokens(action, lookup[cid].token_count)
        return total

    return SelectedCorpus(
        full_tokens=full_tokens,
        datter_tokens=_sum_tokens(datter_ids),
        random_tokens=_sum_tokens(random_ids),
        target_reduction=target_reduction,
        datter_chunk_ids=datter_ids,
        random_chunk_ids=random_ids,
    )
