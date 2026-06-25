"""Production LLM answer + judge for the eval proof loop.

Enable LLM mode
---------------
Set provider keys in the environment before running eval:

- ``OPENAI_API_KEY`` — OpenAI models (gpt55, composer stand-in)
- ``ANTHROPIC_API_KEY`` — Anthropic models (opus, sonnet)

Example::

    export OPENAI_API_KEY=sk-...
    export ANTHROPIC_API_KEY=sk-ant-...
    python scripts/run_paper_summary_team.py --project lab

When no key is present, all entry points fall back to the offline proxy
(``synthesize_answer`` + ``judge_answer`` from ``datter.eval``).

Offline fallback is intentional for hackathon demos and CI — no API spend required.
Paper Summary Team logs ``API required for Paper Summary Team production run`` when offline.
"""

from __future__ import annotations

import json
import logging
import os
import urllib.error
import urllib.request
from dataclasses import dataclass
from enum import Enum
from typing import Callable

import pandas as pd

from datter.eval.answer import synthesize_answer
from datter.eval.judge import judge_answer

logger = logging.getLogger(__name__)

OFFLINE_PST_NOTE = "API required for Paper Summary Team production run"

JUDGE_PROMPT = """You are an eval judge. Score how well the CANDIDATE answer preserves
the REFERENCE answer's meaning for the QUERY. Return JSON only:
{{"score": 0-100, "missing": "brief note or empty string"}}

QUERY: {query}
REFERENCE: {reference}
CANDIDATE: {candidate}
GOLD_HINT (key terms): {gold_hint}"""

ANSWER_PROMPT = """Answer the QUERY using only the CONTEXT below. Be concise (≤120 words).

QUERY: {query}

CONTEXT:
{context}"""


class ModelFamily(str, Enum):
    GPT55 = "gpt55"
    OPUS = "opus"
    SONNET = "sonnet"
    COMPOSER = "composer"


# Cursor Task / chat model slugs (distinct from API fallbacks)
CURSOR_MODEL_SLUGS: dict[ModelFamily, str] = {
    ModelFamily.GPT55: "gpt-5.5-medium",
    ModelFamily.OPUS: "claude-opus-4-8-thinking-high",
    ModelFamily.SONNET: "claude-4.6-sonnet-medium-thinking",
    ModelFamily.COMPOSER: "composer-2.5-fast",
}


def cursor_slug_for(family: ModelFamily) -> str:
    return CURSOR_MODEL_SLUGS[family]


# Best available API ids — document fallbacks inline
MODEL_IDS = {
    ModelFamily.GPT55: ("openai", "gpt-4o"),  # gpt-5.5 unavailable; prefer gpt-4o over o3-mini for judge quality
    ModelFamily.OPUS: ("anthropic", "claude-opus-4-6"),
    ModelFamily.SONNET: ("anthropic", "claude-sonnet-4-6"),
    # Composer is Cursor-internal; fast OpenAI mini stand-in for API runs
    ModelFamily.COMPOSER: ("openai", "gpt-4o-mini"),
}


@dataclass(frozen=True)
class ModelSpec:
    family: ModelFamily
    provider: str
    api_id: str
    available: bool = True
    note: str = ""

    @classmethod
    def from_family(cls, family: ModelFamily) -> ModelSpec:
        provider, api_id = MODEL_IDS[family]
        note = ""
        if family == ModelFamily.GPT55:
            note = "gpt-5.5 unavailable via API; using gpt-4o fallback"
        elif family == ModelFamily.COMPOSER:
            note = "Composer is Cursor-internal; using gpt-4o-mini stand-in"
        return cls(family=family, provider=provider, api_id=api_id, available=True, note=note)

    @classmethod
    def gpt55_fallback(cls) -> ModelSpec:
        return cls.from_family(ModelFamily.GPT55)


def get_model_roster() -> list[ModelSpec]:
    """Paper Summary Team roster: one pair per model family."""
    if not has_llm_keys():
        logger.warning(OFFLINE_PST_NOTE)
    return [ModelSpec.from_family(f) for f in ModelFamily]


def has_llm_keys() -> bool:
    return bool(os.environ.get("OPENAI_API_KEY") or os.environ.get("ANTHROPIC_API_KEY"))


def _http_post(url: str, headers: dict, body: dict) -> dict:
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode(),
        headers={**headers, "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode())


def _openai_chat(prompt: str, model: str = "gpt-4o-mini") -> str:
    key = os.environ.get("OPENAI_API_KEY", "")
    if not key:
        raise RuntimeError("OPENAI_API_KEY not set")
    data = _http_post(
        "https://api.openai.com/v1/chat/completions",
        {"Authorization": f"Bearer {key}"},
        {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.0,
            "max_tokens": 512,
        },
    )
    return data["choices"][0]["message"]["content"].strip()


def _anthropic_chat(prompt: str, model: str = "claude-sonnet-4-6") -> str:
    key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not key:
        raise RuntimeError("ANTHROPIC_API_KEY not set")
    data = _http_post(
        "https://api.anthropic.com/v1/messages",
        {
            "x-api-key": key,
            "anthropic-version": "2023-06-01",
        },
        {
            "model": model,
            "max_tokens": 512,
            "messages": [{"role": "user", "content": prompt}],
        },
    )
    return data["content"][0]["text"].strip()


def llm_complete(prompt: str, model: ModelSpec | None = None) -> str:
    """Unified LLM call routed by ModelSpec provider."""
    if model is None:
        if os.environ.get("OPENAI_API_KEY"):
            return _openai_chat(prompt)
        if os.environ.get("ANTHROPIC_API_KEY"):
            return _anthropic_chat(prompt)
        raise RuntimeError("No LLM API key configured")

    if model.provider == "openai":
        return _openai_chat(prompt, model=model.api_id)
    if model.provider == "anthropic":
        return _anthropic_chat(prompt, model=model.api_id)
    raise RuntimeError(f"Unknown provider: {model.provider}")


def _llm_complete_legacy(prompt: str) -> str:
    return llm_complete(prompt, model=None)


def llm_synthesize_answer(query: str, retrieved_df: pd.DataFrame) -> str:
    """Generate an answer from retrieved chunks; offline fallback when no key."""
    if not has_llm_keys() or retrieved_df.empty:
        return synthesize_answer(query, retrieved_df)

    context_parts = []
    for _, row in retrieved_df.iterrows():
        text = str(row.get("text", ""))[:800]
        if text.strip():
            context_parts.append(text)
    context = "\n---\n".join(context_parts) or "No context."
    prompt = ANSWER_PROMPT.format(query=query, context=context)
    try:
        return llm_complete(prompt)[:1200]
    except (urllib.error.URLError, OSError, KeyError, RuntimeError):
        return synthesize_answer(query, retrieved_df)


def llm_judge_answer(
    query: str,
    reference: str,
    candidate: str,
    gold_hint: str = "",
    model: ModelSpec | None = None,
) -> tuple[float, str]:
    """Score candidate vs reference; offline token-overlap fallback when no key."""
    if not has_llm_keys():
        return judge_answer(reference, candidate, gold_hint)

    prompt = JUDGE_PROMPT.format(
        query=query,
        reference=reference[:800],
        candidate=candidate[:800],
        gold_hint=gold_hint or "(none)",
    )
    try:
        raw = llm_complete(prompt, model=model)
        start = raw.find("{")
        end = raw.rfind("}") + 1
        if start >= 0 and end > start:
            parsed = json.loads(raw[start:end])
            score = float(parsed.get("score", 0))
            missing = str(parsed.get("missing", ""))
            return round(min(100.0, max(0.0, score)), 1), missing
    except (json.JSONDecodeError, urllib.error.URLError, OSError, KeyError, RuntimeError, ValueError):
        pass
    return judge_answer(reference, candidate, gold_hint)


def get_answer_fn() -> Callable[[str, pd.DataFrame], str]:
    return llm_synthesize_answer if has_llm_keys() else synthesize_answer


def get_judge_fn() -> Callable[[str, str, str], tuple[float, str]]:
    if has_llm_keys():
        return lambda ref, cand, hint: llm_judge_answer("", ref, cand, hint)
    return lambda ref, cand, hint: judge_answer(ref, cand, hint)
