---
type: product
status: active
created: 2026-06-25
updated: 2026-06-25
tags:
  - product
  - orchestration
  - eval
  - paper-summary-team
source: ceo-steer-2026-06-25
---

# Paper Summary Team

Multi-model **CTO eval loop** that proves compressed corpus preserves downstream understanding — one examiner/examinee pair per model family, same family judges fairly.

## Purpose

For each PDF project, compare **full corpus text** vs **compressed/optimised export**:

1. Spawn eval pairs per model family: **gpt-5.5**, **opus**, **sonnet**, **composer** (2 roles each)
2. **FULL** agent generates exam questions where full context definitely has the answer
3. **COMPRESSED** agent answers from optimised corpus only
4. **FULL** agent (same model family) scores compressed answers — target **100%** understanding match
5. If score &lt; quality floor: **compressor regenerates** with tighter strategy (max 6 iterations)
6. On pass: record **exam tokens** (full vs compressed) and **compression ratio**
7. Business insight: Pareto frontier — e.g. 80% token save acceptable if score drops 100%→90%
8. Future: image compress teams; today **PDF/text only**

## Model roster

| Family | Examiner role | Examinee role | API id (2026-06) | Provider |
|---|---|---|---|---|
| **gpt55** | FULL — build exam + score | COMPRESSED — answer | `gpt-4o` (gpt-5.5 fallback) | OpenAI |
| **opus** | FULL | COMPRESSED | `claude-opus-4-6` | Anthropic |
| **sonnet** | FULL | COMPRESSED | `claude-sonnet-4-6` | Anthropic |
| **composer** | FULL | COMPRESSED | `gpt-4o-mini` stand-in | OpenAI (Cursor-internal) |

Env vars: `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`. See [[Multi-Model Exam Loop]] for flow diagram.

## Exam protocol

```text
For each model family M in roster:
  1. build_exam(corpus_full, M) → questions + reference answers (FULL context)
  2. answer_exam(corpus_compressed, questions, M) → candidate answers
  3. score_exam(reference, candidate, M) → 0–100 per Q + aggregate

Aggregate pass: min score across all families ≥ quality_floor (default 1.0 = 100%)

If fail:
  regenerate_compressed() — lower reduction step, higher relevance boost, tighter keep
  retry up to max_iterations (6)
```

## Retry loop (compressor)

| Iteration | Adjustment |
|---|---|
| 0 | Pareto max safe cut @ project quality floor |
| 1+ | `target_reduction -= 5%`; `relevance_boost += 0.10` |

Record best Pareto point: `(compression_pct, min_score_across_models, tokens_full, tokens_compressed)`.

## Outputs

| Artifact | Path |
|---|---|
| Exam corpus | `{project}/exam_corpus/full_corpus.txt`, `compressed_iter_N.txt` |
| Results JSON | `{project}/exam_results.json` |
| CLI | `python scripts/run_paper_summary_team.py --project lab` |

Code: `datter/eval/paper_summary_team.py`, `datter/eval/llm_judge.py`.

## Pareto → pricing

Score vs compression tradeoff drives tier selection for AI lab ICP — see [[Business Model & Finance]] § Paper Summary Team → pricing.

Example business question: *"At 80% token reduction, does understanding stay ≥90% across gpt, opus, sonnet?"* — that point maps to **Standard** tier; 95%+ maps to **Assured**.

## Offline fallback

No API keys → TF-IDF judge + token overlap (same as [[Proof Loop Spec]]). Logs: *"API required for Paper Summary Team production run"*. CI and hackathon demos use offline path; AI lab pilots require live multi-model run.

## Links

- Technical flow: [[Multi-Model Exam Loop]]
- Proof baseline: [[Proof Loop Spec]]
- Business: [[Business Model & Finance]]
- Outreach: [[Business Outreach Brief]]
- Handoff: [[HANDOFF]]
