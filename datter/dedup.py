from __future__ import annotations

import hashlib
import re
from collections import defaultdict

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from datter.models import Chunk

NEAR_DUP_THRESHOLD = 0.85


def normalize_for_hash(text: str) -> str:
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\w\s]", "", text)
    return text.strip()


def exact_hash(text: str) -> str:
    return hashlib.sha256(normalize_for_hash(text).encode("utf-8")).hexdigest()


class UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.parent[rb] = ra


def mark_exact_duplicates(chunks: list[Chunk]) -> None:
    groups: dict[str, list[int]] = defaultdict(list)
    for i, chunk in enumerate(chunks):
        groups[exact_hash(chunk.text)].append(i)

    for group_id, indices in groups.items():
        if len(indices) < 2:
            continue
        canonical_idx = max(indices, key=lambda i: (chunks[i].token_count, len(chunks[i].text)))
        for i in indices:
            chunks[i].is_exact_duplicate = True
            chunks[i].exact_dup_group = group_id
            chunks[i].is_canonical = i == canonical_idx
            if i != canonical_idx:
                chunks[i].max_similarity = max(chunks[i].max_similarity, 1.0)


def mark_near_duplicates(chunks: list[Chunk], threshold: float = NEAR_DUP_THRESHOLD) -> None:
    if len(chunks) < 2:
        return

    texts = [c.text for c in chunks]
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1, stop_words="english")
    matrix = vectorizer.fit_transform(texts)
    sim = cosine_similarity(matrix)

    uf = UnionFind(len(chunks))
    for i in range(len(chunks)):
        for j in range(i + 1, len(chunks)):
            if sim[i, j] >= threshold:
                uf.union(i, j)
                chunks[i].max_similarity = max(chunks[i].max_similarity, float(sim[i, j]))
                chunks[j].max_similarity = max(chunks[j].max_similarity, float(sim[i, j]))

    cluster_map: dict[int, list[int]] = defaultdict(list)
    for i in range(len(chunks)):
        cluster_map[uf.find(i)].append(i)

    for root, members in cluster_map.items():
        if len(members) < 2:
            continue
        group_id = f"near_{root}"
        for i in members:
            chunks[i].near_dup_group = group_id


def deduplicate_chunks(chunks: list[Chunk]) -> list[Chunk]:
    mark_exact_duplicates(chunks)
    mark_near_duplicates(chunks)
    return chunks


def duplicate_stats(chunks: list[Chunk]) -> tuple[float, float]:
    if not chunks:
        return 0.0, 0.0
    exact = sum(1 for c in chunks if c.is_exact_duplicate)
    near = sum(1 for c in chunks if c.near_dup_group is not None)
    n = len(chunks)
    return exact / n, near / n
