---
type: product
status: active
created: 2026-06-25
updated: 2026-06-25
tags:
  - product
  - orchestration
  - hackathon
  - datter
source: ceo-chat-2026-06-25
---

# Orchestration Plan

Master index for multi-agent work **before and during** hackathon execution. Tharm orchestrates from the **CEO chat**; agents coordinate via this folder, [[HANDOFF]], and [[REQUESTS]].

## Read this when

- Starting a multi-agent build loop (CEO says "orchestrate")
- CTO/CPO chats need context without re-reading the whole CEO thread
- Priorities shifted from ML-paper demo → vertical proof + project UX

## Sub-documents (read targeted note only)

| Note | Owns |
|---|---|
| [[Agent Team Model]] | CEO / CTO / CPO chats + pipeline agents + internal handoff |
| [[Project Model]] | Create-project-first UX; corpus boundaries; business framing |
| [[Hackathon Win Strategy]] | Official criteria, demo format, reframe for Hands Off |
| [[Vertical Demo Corpus]] | 4 domain PDFs to download; folder layout; eval questions TODO |
| [[Proof Loop Spec]] | 50% cut @ 90% understanding; LLM judge; Pareto curve; no Adisorn |
| [[CEO Discussion Archive 2026-06-25]] | Decisions from CEO chat not yet in code |

## Current strategic decisions (locked)

1. **Company = selection engine** — find max token cut at a quality floor, not blind delete.
2. **Hackathon demo corpus** — diverse real-world PDFs (social / gov / engineering / science), **not** the 8 ML paper notes in `brain/01_Research/Papers/`.
3. **Proof** — LLM answer + LLM judge loop; target **≥90% understanding at ~50% token cut**; always compare **Datter vs random** at same budget.
4. **Scorer for now** — **baseline only**; **Adisorn deferred** until model files arrive.
5. **Project scoping** — user must **create a project** before upload/score; no cross-project scoring (e.g. one simulation campaign = one project).
6. **Parallel tracks** when orchestrating: Engine (CTO) + UX (CPO) + Business/pricing (CEO/CPO) — see phases below.

## Orchestration phases

### Phase 0 — CEO (before code)

- [ ] Download PDFs from [[Vertical Demo Corpus]] into `demo_verticals/{social,gov,engineering,science}/`
- [ ] Draft `queries.json` per vertical (6–8 questions each) — or delegate to CPO
- [ ] Confirm API key strategy for LLM judge (pre-run + cache for live demo)

### Phase 1 — Parallel

| Track | Owner | Deliverable |
|---|---|---|
| A Proof loop | CTO | `datter/eval/` or script; M4-lite; baseline only |
| B Project UX | CPO → CTO | Project create → upload → run; spec in [[Project Model]] |
| C Dashboard | CPO → CTO | Hero ICP, Proof tab, Pareto chart, agent streaming |
| D Business | CEO/CPO | Pricing tied to quality floor; [[Business Strategy]] addendum |

### Phase 2 — Integrate

- Streamlit: project selector → vertical/corpus → agents → savings + **understanding %** + curve
- 2-min Loom + hackathon submit ([[Hackathon Win Strategy]])

### Phase 3 — Defer (post-hackathon)

- M2 greedy selector; PhD simulation CSV ingest; Adisorn; full training eval (CNN-style)

## Agent internal discussion rule

Chats do not talk to each other. **Write to [[HANDOFF]]** with tags:

- `[CEO → CTO]` — build spec
- `[CEO → CPO]` — UX/copy
- `[CTO → CEO]` — blockers, tradeoffs, done
- `[CPO → CEO]` — journey decisions

Active queue stays in [[REQUESTS]].

## Links

- Up: [[Project Map]]
- Product: [[Product Spine]], [[Business Strategy]]
- MVP today: [[Hackathon MVP Summary]]
- Experiments: [[Experiment Map]]
