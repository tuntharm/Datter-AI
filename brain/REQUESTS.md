# REQUESTS.md - Active Datter AI Requests

This file is the active queue for concrete build tasks. Orchestration context: `brain/02_Product/Orchestration/Orchestration Plan.md`.

Review loop: [[Multi-Model Review Loop]] · Round 1 outcomes: [[CEO Review Meeting 2026-06-25]]

## Pending — P0 Review Round 2 (from multi-model critique)

- [ ] P0 **Beat random on eval** — Datter ties random (0 pp) on all 5 projects after relevance boost.
  - Files: `datter/selection.py`, `datter/eval/relevance_boost.py`, `datter/eval/pareto.py`
  - Acceptance: `(understanding_pct − random_understanding_pct) > 0` on **government** and **lab**
  - Context: [[Multi-Model Review Loop]] gate
  - **Partial 2026-06-25** — gov floor pass + max cut 20%→50%; delta still 0 pp everywhere

- [ ] P0 **Lab quality floor** — 85.9% understanding @ 40.9% cut; misses 90% floor.
  - Files: `demo_data/queries.json`, `datter/selection.py`, eval harness
  - Acceptance: `meets_quality_floor = true` on lab OR document eval/corpus misalignment in brain
  - Note: duplicate-aware eval questions may conflict with non-canonical dup drop policy

- [ ] P0 **Production LLM judge** — investor/client blocker for fundable / embeddable claim.
  - Files: `datter/eval/llm_judge.py`, [[Proof Loop Spec]]
  - Acceptance: gov + lab run through LLM answer + judge; disclaimer updated in app
  - **Stub done 2026-06-25** — `has_llm_keys()`, offline fallback; wire into `run_eval_loop` + app disclaimer next

- [x] P0 **Query relevance in selection (M3-lite)** — gold-hint boost for SelectAgent.
  - Files: `datter/eval/relevance_boost.py`, `datter/selection.py`, `datter/agent.py`, `datter/eval/pareto.py`, `tests/test_relevance_boost.py`
  - **Done 2026-06-25** — gov max cut 20%→50%, floor pass on 4/4 verticals; boost in `select_datter_cut()`

- [x] P0 **LLM judge stub (no API key)** — interface + offline fallback.
  - Files: `datter/eval/llm_judge.py`
  - **Done 2026-06-25** — enable via `OPENAI_API_KEY` or `ANTHROPIC_API_KEY`; no keys in env tonight

- [x] P0 **Stale eval cache invalidation** — pareto fields missing caused wrong cuts.
  - Files: `datter/agent.py`, `demo_verticals/*/eval_cache.json`, `demo_data/eval_cache.json`
  - **Done 2026-06-25** — caches deleted + refreshed; guard when `max_safe_reduction_pct == 0`

## Pending — P0 Hackathon (orchestrate these first)

- [x] P0 **Proof loop (M4-lite)** — offline TF-IDF + token overlap judge; Proof tab in app
  - Files: `datter/eval/`, `demo_verticals/*/queries.json`, `app.py` Proof tab
  - Note: building demo proxy only; LLM judge deferred

- [x] P0 **Project-first UX (minimal)** — project picker with vertical PDFs + Lab
  - Files: `datter/project.py`, `app.py`
  - Session state; disk `projects/<id>/` deferred

- [x] P0 **Agent autonomy demo** — streaming log + hands-off auto-run + Select + Eval agents
  - Files: `datter/agent.py`, `app.py`

- [x] P0 **Outcome-first dashboard copy** — Outcome/Proof/Export/Executive tabs
  - Files: `app.py`, `Demo UX Spec.md`, `Executive Finance Report.md`

## Pending — P1 (after P0 or parallel if staffed)

- [ ] P1 **Social vertical frontier** — max safe cut stuck at 20% despite floor pass.
  - Files: `datter/scorers/`, `datter/eval/relevance_boost.py`
  - Acceptance: max_safe_reduction_pct ≥ 35% on social without dropping below floor
  - Context: Round 1 investor/client objection

- [ ] P1 Implement greedy marginal selector under token budget (M2).
  - Files: `datter/selection.py` (new), `datter/agent.py`, `datter/report.py`, `app.py`
  - Acceptance: selected subset maximises score-per-token; demo shows subset vs independent thresholding.
  - Context: [[Product Spine]]

- [ ] P1 Add task description + representative queries to scoring (M3).
  - Files: `app.py`, `datter/scorers/baseline.py`, `datter/eval/relevance_boost.py`
  - Acceptance: task-conditioned relevance visible in chunk scores; uses project `queries.json`
  - Context: [[Product Spine]], [[Proof Loop Spec]]
  - Note: M3-lite shipped in relevance_boost; extend to scorer + marginal selector

- [ ] P1 Export optimised corpus (keep chunks only) — make "compress" tangible.
  - Files: `datter/export.py`, `app.py`
  - Acceptance: download folder/zip of selected text chunks + manifest
  - **Done 2026-06-25** — zip export in Export tab

- [x] P1 CPO: Pareto chart + AI-lab CEO pricing worksheet in brain.
  - Files: `brain/02_Product/Orchestration/Business Model & Finance.md`, `Executive Finance Report.md`
  - Acceptance: quality floor + max safe cut SKU + pricing tiers + research flywheel

- [ ] P1 **Research team — scorer frontier** — hire/improve until max cut rises at fixed floor.
  - Files: `datter/scorers/`, `datter/selection.py`, `datter/eval/`
  - Acceptance: on lab corpus, max_safe_reduction_pct increases vs baseline; gov corpus Datter ≥ random on production judge (future)
  - Context: [[Business Model & Finance]]

- [ ] P1 Wire Adisorn model when files arrive (M5).
  - Files: `datter/scorers/adisorn_complexity.py`, `models/adisorn/`
  - Blocker: need model format + output semantics from Adisorn.
  - **Still needs Adisorn/training** — baseline-only tonight; hybrid unlocks gov/social frontier

- [ ] P1 Decide action vocabulary: keep/drop/compress/review vs keep/exclude/consolidate/compress/review.
  - Context: [[Product Spine]], [[CEO Discussion Archive 2026-06-25]]

- [ ] P1 Compression-alignment experiment inspired by [[ZIP-FIT]].
  - Context: research track, not hackathon demo corpus

- [ ] P2 Simulation CSV project type (PhD vision).
  - Spec: [[Project Model]], [[CEO Discussion Archive 2026-06-25]]
  - Acceptance: ingest case files; IC-hash dedup stub

- [ ] P2 Embedding semantic-dedup baseline ([[SemDeDup]]).

## Completed

- [x] 2026-06-25 Hackathon MVP: Streamlit app, agent pipeline, scorer plugins, demo data, tests.
- [x] 2026-06-25 Archive Cursor session + product spine into `brain/02_Product/`.
- [x] 2026-06-25 Create project-local Datter brain and paper routing layer.
- [x] 2026-06-25 Review Round 1: relevance boost, exec tab warnings, brain review docs, 18 tests.
- [x] 2026-06-25 CTO round: query-boost in selection.py, llm_judge stub, cache refresh, 19 tests.

## Questions / Blockers

- [ ] Adisorn model semantics — **deferred**, baseline only; hybrid scorer needs Adisorn training deliverable.
- [ ] LLM judge provider + key for proof loop — **stub ready** (`datter/eval/llm_judge.py`); set `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` to enable.
- [ ] Tharm: download [[Vertical Demo Corpus]] PDFs into `demo_verticals/`.
