from __future__ import annotations

import re


def _token_set(text: str) -> set[str]:
    return set(re.findall(r"\b\w+\b", text.lower()))


def judge_answer(reference: str, candidate: str, gold_hint: str = "") -> tuple[float, str]:
    ref_tokens = _token_set(reference)
    cand_tokens = _token_set(candidate)
    if not ref_tokens:
        return 0.0, "No reference answer available."

    overlap = len(ref_tokens & cand_tokens) / len(ref_tokens)
    score = min(100.0, overlap * 100.0)

    missing_parts: list[str] = []
    if gold_hint:
        hint_tokens = _token_set(gold_hint)
        missing = hint_tokens - cand_tokens
        if missing:
            missing_parts.append(f"Missing key terms: {', '.join(sorted(missing)[:8])}")

    if score < 70 and not missing_parts:
        ref_words = reference.split()[:20]
        missing_parts.append(f"Low overlap with full-corpus answer (first terms: {' '.join(ref_words[:12])}...)")

    return round(score, 1), "; ".join(missing_parts) if missing_parts else ""
