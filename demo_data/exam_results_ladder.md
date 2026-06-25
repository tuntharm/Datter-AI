# Compression ladder — lab project

**Run:** 2026-06-25 · **Quality floor:** 90% · **Judge:** offline TF-IDF fallback (no API keys)

## Summary

| Metric | Value |
|--------|-------|
| Best compression at floor | **None** — no step met 90% min score |
| Best min score observed | 85.9% at 40.9% actual reduction (minimum achievable on demo corpus) |
| Steps run | 1 (stopped early: min_score &lt; floor) |
| API mode | `offline` |

**Judge note:** API required for Paper Summary Team production run — using TF-IDF judge fallback.

**Corpus note:** Ladder evaluated on canonical demo files `01–06` only. `exam_prompts/*.md` in `demo_data/` are ingested by the lab project but excluded here (they pollute scores when included). `exam_corpus/` is already skipped by ingest.

## Ladder table

| Step | Target reduction | Actual reduction | Tokens full | Tokens compressed | Min score | Passed |
|------|------------------|------------------|-------------|-------------------|-----------|--------|
| 1 | 10% | 40.9% | 685 | 405 | 85.9% | No |

Steps 2–8 were not run (early stop at step 1).

At targets 10–40%, actual reduction stays at 40.9% (4 non-drop chunks, 405 tokens). Higher targets increase reduction (55.9% at 50%, 76.4% at 70%) but scores fall further (77.8% → 65.8%).

## Root cause

1. **Baseline scorer drops canonical duplicates:** `01_unique_research_note.md` is `is_canonical=True` but gets `recommended_action=drop` because `redundancy ≥ 0.92` fires before the canonical guard. Q1 (unique research findings) cannot be answered from compressed corpus.
2. **Selection skips all `drop` chunks:** Minimum compression on demo corpus is ~41%, not the 10–20% ladder start the experiment intended.
3. **Offline judge ceiling:** TF-IDF overlap judge scores ~86% max on this corpus even at minimum compression; live multi-model judge needed for production floor checks.

## Compressor recommendation

1. **Keep canonical chunks** even when redundancy is high — adjust `recommend_action()` in `baseline.py` so `is_canonical` bypasses the `redundancy ≥ 0.92` drop rule.
2. **Query-relevance boost before cut:** Ensure `apply_query_relevance_boost` lifts query-critical chunks (e.g. unique note for q1) above drop threshold.
3. **Exclude eval artifacts from ingest:** Skip `exam_prompts/` (and already `exam_corpus/`) in `ingest_folder` so lab reruns stay clean.
4. **Re-run ladder with API keys** after scorer fix for authoritative 90% floor measurement.
