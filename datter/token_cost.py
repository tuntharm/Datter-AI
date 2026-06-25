from __future__ import annotations

import tiktoken

DEFAULT_TOKEN_COST_PER_M = 0.15
DEFAULT_EMBEDDING_COST_PER_M = 0.02
ENCODING_NAME = "cl100k_base"

_enc = None


def get_encoding():
    global _enc
    if _enc is None:
        _enc = tiktoken.get_encoding(ENCODING_NAME)
    return _enc


def count_tokens(text: str) -> int:
    if not text:
        return 0
    return len(get_encoding().encode(text))


def estimate_token_cost(tokens: int, cost_per_m: float = DEFAULT_TOKEN_COST_PER_M) -> float:
    return (tokens / 1_000_000) * cost_per_m


def estimate_embedding_cost(tokens: int, cost_per_m: float = DEFAULT_EMBEDDING_COST_PER_M) -> float:
    return (tokens / 1_000_000) * cost_per_m
