---
type: map
status: active
created: 2026-06-25
updated: 2026-06-25
tags:
  - experiment
  - map
  - datter
---

# Experiment Map

## Purpose

This note routes Datter validation work: what the app proves, what it does not prove yet, and which paper ideas should become tests.

## Current Evidence Surface

| Evidence | Read |
|---|---|
| Bundled demo corpus | `demo_data/` |
| End-to-end run logic | `datter/agent.py` |
| Exact/near duplicate behavior | `datter/dedup.py`, `tests/test_dedup.py` |
| Scoring behavior | `datter/scorers/baseline.py`, `tests/test_scorers.py` |
| Report outputs | `datter/report.py`, `tests/test_agent.py` |
| UI demo | `app.py` |

## Current Baseline Hypothesis

Datter can use local redundancy, novelty, information-density, and gzip-complexity proxies to identify avoidable AI spend before tokenization, embedding, retrieval, or training.

## Experiment Backlog

| Priority | Experiment | Paper Link | Success Signal |
|---|---|---|---|
| P1 | Compression-alignment baseline for a target task/query | [[ZIP-FIT]] | Selected chunks improve relevance versus current baseline |
| P1 | Reweight/compress recommendation instead of binary drop | [[SoftDedup]] | Recommendations preserve useful repeated content while reducing avoidable tokens |
| P1 | Exact/near/semantic dedup comparison | [[Deduplicating Training Data Makes Language Models Better]], [[SemDeDup]] | Clear tradeoff between cheap dedup and embedding dedup |
| P2 | Predictive data-value proxy | [[Predictive Data Selection]] | Score predicts downstream retrieval or QA usefulness |
| P2 | Curated-subset condition check | [[Why Less is More Sometimes]] | Identify when dropping data harms versus helps |
| P2 | Usefulness versus compressibility analysis | [[Understanding LLM Behaviors via Compression]] | Avoid confusing low entropy with high usefulness |

## Do Not Claim Yet

- Do not claim Datter improves downstream model performance until tested.
- Do not claim universal data value scoring from gzip alone.
- Do not cite exact paper metrics unless the relevant note has `read_depth: full`.

## Links

- Up: [[Project Map]]
- Source: [[Source Map]]
- Papers: [[Papers Map]]
- Queue: [[Paper Queue]]

