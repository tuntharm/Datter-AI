---
type: session
status: archived
created: 2026-06-25
updated: 2026-06-25
tags:
  - ceo
  - chat
  - orchestration
  - handoff
source: cursor-ceo-chat-2026-06-25
---

# CEO Discussion Archive 2026-06-25

Archive of CEO Cursor chat decisions **before** multi-agent orchestration run. For execution specs see [[Orchestration Plan]] and [[REQUESTS]].

## Chat roles agreed

- **CEO chat** (main) — strategy, orchestrate, handoffs
- **CTO chat** — build, often
- **CPO chat** — UX/product, rarely
- Internal coordination via [[HANDOFF]] + [[REQUESTS]], not chat-to-chat

## Key pivots from discussion

### Demo corpus

- Rejected: ML research papers (ZIP-FIT etc.) as customer demo input
- Accepted: **4 vertical PDFs** — social, government, engineering, science ([[Vertical Demo Corpus]])
- 8 paper **notes** in `brain/01_Research/Papers/` stay for scoring research only

### Proof method

- Rejected for tonight: physics simulation orchestration, CNN retrain demo
- Accepted: **LLM answer + LLM judge** on fixed questions; loop until **≥90% at ~50% token cut**
- Always compare **Datter vs random** at same token budget
- Product = **Pareto curve** (max cut at quality floor), not fixed promise

### Scoring

- **Adisorn off** until model files received
- Baseline only for hackathon proof loop
- Scores alone insufficient — **eval set required** ([[Proof Loop Spec]])

### "Compress" honesty

- MVP does **not** gzip or rewrite PDFs
- Recommends keep/drop/compress/review; **compress** = consolidate/trim before embed
- Future: export optimised corpus folder

### Project-first UX

- Cannot score unrelated uploads together
- User **creates project** → adds corpus + task + eval questions → run agents ([[Project Model]])
- Simulation batch = one project (future CSV ingest)

### PhD / beam data

- Authentic moat later; **not** hackathon primary demo
- PhD thesis notes stay in PhD brain; optional future `demo_verticals/engineering/` sim pack

### Hackathon

- Official site: agent autonomy, UX, real-world applicability ([[Hackathon Win Strategy]])
- Reframe: autonomous agent **company**, not chunk dashboard
- Streamlit UX weak — CPO parallel track for outcome-first UI

### Business (parallel, not after engineering)

- Think as **AI lab CEO**: would they pay for max cut at 90% floor?
- Pricing: free audit → $/M tokens / project → enterprise SLA on quality floor

## Physics simulation vision (deferred, captured)

- Upload N simulation cases; flag same initial inputs; score entropy/complexity; ignore repeats
- Maps to regime model in [[Business Strategy]] and Adisorn time_series input type
- Requires CSV/feature ingest — not in MVP

## Open before orchestrate

- [ ] Tharm downloads PDFs ([[Vertical Demo Corpus]])
- [ ] Draft queries.json per vertical
- [ ] LLM API key + pre-run cache strategy
- [ ] More discussion items from Tharm may arrive — append here or [[HANDOFF]]

## Links

- Up: [[Orchestration Plan]]
- [[Agent Team Model]]
- [[Project Model]]
