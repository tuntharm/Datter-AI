---
type: product
status: active
created: 2026-06-25
updated: 2026-06-25
tags:
  - product
  - eval
  - proof
source: ceo-chat-2026-06-25
---

# Proof Loop Spec

How Datter proves a cut is safe — **AI uses AI** to score understanding.

## Core claim (honest)

> At a **token budget** (target ~50% reduction), Datter preserves **≥90% understanding** vs the full corpus, measured by an LLM judge on fixed questions — better than **random** cut at the same size.

Not: "compress PDF files on disk."  
Yes: "minimum token corpus for downstream AI at your quality floor."

## Why a test set is mandatory

Baseline scorer today has **no downstream signal** — see `datter/scorers/baseline.py`. Without [[Vertical Demo Corpus]] `queries.json`, scores are structural guesses only.

Eval set drives:

1. Proof after cut (M4-lite)
2. Task relevance in scoring (M3)
3. Future selector feedback (M2 + M4)

## Protocol

```text
For each project / vertical:
  1. FULL: all chunks → answer LLM answers Q1..Qn
  2. DATTER_CUT: reduce to ~target_token_reduction using baseline keep/drop/compress
  3. RANDOM_CUT: random chunk drop to same token count as DATTER_CUT
  4. JUDGE: score each (cut answer vs FULL answer) 0–100 per question
  5. LOOP (optional): if mean < quality_floor, loosen cut (45%, 40%...) max 6 iterations
  6. PARETO: record (token_%, understanding_%) points for chart
```

## Constants (defaults)

| Param | Value |
|---|---|
| `target_token_reduction` | 0.50 (50%) |
| `quality_floor` | 0.90 (90%) |
| `max_iterations` | 6 |
| `scorer_mode` | **baseline only** — Adisorn off |
| `compare_baseline` | random cut at same token budget |

## LLM roles

| Role | Input | Output |
|---|---|---|
| Answer | context (full or reduced text) + question | short answer |
| Judge | reference answer (from FULL) + candidate answer | `{score: 0-100, missing: "..."}` |

Pre-run and cache results for live demo; API key required for full automation.

## Offline fallback

TF-IDF retrieval recall@3 on `gold_chunk_id` if LLM unavailable — weaker but no network.

## Business link (Pareto)

Product sells **max cut at customer's quality floor**, not fixed 50%/90% for all data. Chart: token reduction % vs understanding %. See [[Project Model]] and [[Business Strategy]].

## CTO acceptance

- [ ] Script or `datter/eval/` module runs protocol on one vertical PDF
- [ ] Streamlit **Proof** tab shows Datter % vs Random % at target cut
- [ ] Reduction curve JSON exportable
- [ ] Does not claim quality preservation without running eval

## Deferred

- CNN / training accuracy eval (Phase 2 ML-lab buyer)
- PhD simulation surrogate error
- Adisorn in score loop

## Links

- Up: [[Orchestration Plan]]
- Corpus: [[Vertical Demo Corpus]]
- Experiments: [[Experiment Map]]
