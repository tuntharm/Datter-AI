---
type: product
status: active
created: 2026-06-25
updated: 2026-06-25
tags:
  - product
  - ux
  - projects
source: ceo-chat-2026-06-25
---

# Project Model

## Problem

Today the app accepts a folder or ad-hoc uploads with **no boundary**. Scoring across unrelated data is wrong:

- Simulation run 1–10 belong to **one campaign** (same IC space, same task)
- Gov PDFs and a random wiki export should **not** be scored as one corpus
- Dedup, redundancy, and eval questions are **project-scoped**

> You cannot score "the whole drive" — only a **defined corpus + task + eval set**.

## Product concept: Project-first

```text
1. Create project
   - name, description
   - domain tag (RAG / simulation / gov / custom)
   - task description (what downstream AI must do)
   - quality floor (e.g. 90% understanding)
   - token budget target (e.g. 50% reduction)

2. Add corpus to project
   - upload PDFs/MD/TXT (today)
   - future: CSV sim runs, JSONL fine-tune rows

3. Add eval set (required for proof)
   - queries.json or Q&A pairs
   - used by EvalAgent — see [[Proof Loop Spec]]

4. Run agent pipeline (scoped to this project only)

5. Output
   - audit trail, recommended corpus, Pareto curve for THIS project
```

## Business framing (AI lab CEO lens)

| Without projects | With projects |
|---|---|
| "We analyse files" | "We optimise **your RAG corpus for support bot X**" |
| Meaningless global score | **Maximum cut at your quality floor** |
| No pricing unit | Price per **project** or per **M tokens analysed** within project |
| No rollback | Project manifest: what was dropped and why |

**Offer:** "Pick your quality floor (90–99%). We find the largest token cut that preserves it."

Pricing tiers attach to **quality floor + number of projects** — see [[Business Strategy]] Phase 1 path.

## UX flow (CPO → CTO)

```text
Landing → "New project" → name + task + quality floor
       → Upload corpus (drag-drop, multiple files)
       → Add eval questions (paste or upload queries.json)
       → "Run audit" → streaming agents
       → Results: tokens saved | understanding % | Pareto | export
```

Keep **demo_verticals/** as pre-built example projects for hackathon (one-click load).

## MVP implementation ladder

| Step | Scope | Hackathon? |
|---|---|---|
| 1 | Session-state "project name" + folder path per run | Optional |
| 2 | `projects/<id>/` on disk: corpus + queries.json + report.json | Yes if time |
| 3 | Supabase persistence | Defer |
| 4 | Simulation CSV as project type | Defer |

## Simulation note (PhD vision — deferred)

One project = one batch of runs (e.g. 10 files, same experiment family). Dedup on **initial condition hash** + trajectory similarity — not in MVP ingest. Document here so agents do not mix sim data with RAG docs in one score pass.

## Links

- Up: [[Orchestration Plan]]
- Proof: [[Proof Loop Spec]]
- GTM: [[Business Strategy]]
