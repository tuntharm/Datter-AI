---
type: product
status: active
created: 2026-06-25
updated: 2026-06-25
tags:
  - product
  - orchestration
  - ceo
  - review
source: orchestration-integrator-2026-06-25
---

# CEO Review Meeting — 2026-06-25 (Round 1)

Simulated multi-persona review after full product run on all five projects. Numbers from live pipeline run (offline TF-IDF proxy, post relevance-boost fix).

## CEO pitch (~2 min)

Datter is a **selection engine**, not a dedup dashboard. Customers pick a **quality floor** — e.g. 90% understanding on their eval questions — and we find the **largest token cut** that preserves it.

Tonight's demo runs a **hands-off seven-agent pipeline** on real PDFs: ingest → chunk → dedup → score → **Pareto scan for max safe cut** → eval proof → export. The SKU is **max safe reduction % @ floor**, backed by **Datter vs random at the same token budget**.

Our north star: **same understanding for AI, maximum token drop.** Research (Adisorn, M2 marginal selector, M3 task scoring) pushes the frontier outward — more tokens removed at the same floor — which directly maps to pricing tiers (Standard 90%, Assured 95%, Governed 99%).

**Live proof tonight (all five projects):**

| Project | Tokens | Max safe cut | Understanding @ cut | Random @ budget | Meets 90% floor |
|---|---:|---:|---:|---:|---|
| Government | 131,324 | **50.0%** | 90.1% | 90.1% | Yes |
| Engineering | 34,811 | **45.3%** | 96.1% | 96.1% | Yes |
| Science | 22,103 | **61.2%** | 91.6% | 91.6% | Yes |
| Social | 161,321 | **20.0%** | 94.7% | 94.7% | Yes |
| Lab | 685 | 40.9% | 85.9% | 85.9% | **No** |

Lead vertical for eval story: **Government — 50% token cut at 90.1% understanding.** Lead structural story: **Lab — 40.9% avoidable** (duplicates/boilerplate), but eval proxy misses floor.

---

## Investor persona — AI infra VC

**Questions**

1. **Moat:** Dedup tools exist. Why isn't this a feature flag in a vector DB?
2. **Proof:** TF-IDF + token overlap isn't a production accuracy claim. What unlocks fundable narrative?
3. **Pricing:** $/M tokens analysed at 90/95/99 floors — is that 10× embedding cost or 0.1×?
4. **Flywheel:** You say research lifts max cut. Show me one iteration where frontier moved.

**Verdict:** *Conditional interest.* Product framing (max cut @ floor, agent company, project-scoped eval) is sharper than "we delete duplicates." **Round 1 proof is not yet investable** — offline proxy, Datter **ties random on every project** (0 pp delta), and Lab misses floor.

**Objections**

- "50% cut on a handbook with 90.1% proxy score is thin margin above floor — one bad question breaks the tier."
- "Structural avoidable % on PDFs is ~0–2%; the economic story is eval-driven cut, not audit flags."
- "No LLM judge = no defensible accuracy metric for seed diligence."

---

## Client persona — RAG lead at AI company

**Questions**

1. **Integration:** Do I upload corpus + eval JSON, or wire an API into our ingest pipeline?
2. **Trust:** If you cut 50% of our Treasury PDF, how do I explain misses to compliance?
3. **Audit:** Can I export which chunks were dropped and why, tied to each eval question?
4. **Same-understanding guarantee:** What happens when your proxy says 90% but our production bot drops?

**Verdict:** *Pilot-curious, not production-ready.* Would run a **2-week design partner** on one internal KB if export + manifest are solid. Will **not** embed optimised corpus without LLM-judge proof and a signed quality-floor SLA.

**Objections**

- "Random cut at the same token budget scores the same as Datter on your numbers — why pay you?"
- "Social vertical only achieves 20% max cut; our corpus might look like that, not like science at 61%."
- "Lab misses your own 90% floor — hard to trust the selector on messy real data."

---

## CEO response to objections

| Objection | Response |
|---|---|
| Random ties Datter | Honest tonight: proxy + budget-matched random is a hard bar on dense PDFs. **Round 1 shipped query/gold-hint relevance boost** — gov went from 20% cut @ 88% (fail) to **50% @ 90.1% (pass)**. Next: M2 marginal selector + production judge to **win on delta**, not just floor. |
| Thin margin above floor (gov 90.1%) | Correct — that's why we sell **floor tiers**, not point estimates. Assured/Governed buyers pay for headroom; Standard is the wedge. |
| Structural avoidable ~0% on PDFs | Audit tab is the wedge; **SKU is eval-max cut**. CFO leads with token removal @ floor, not avoidable %. |
| No LLM judge | [[Proof Loop Spec]] harness is P0 post-hackathon. Tonight: relative win + disclaimer; seed unlock = LLM judge on 2 design-partner corpora. |
| Lab misses floor | Lab proves **structural waste** (41% avoidable); eval set needs tuning for duplicate-aware questions. Demo Lab for savings; demo **Gov/Science** for eval proof. |
| Vector DB feature | We own **project-scoped eval + Pareto scan + research flywheel** — the loop that moves max cut, not one-time dedup. |

---

## Round 2 update (2026-06-25, post query-boost re-run)

Fresh run with deleted caches + `queries_path` wired through `selection.py`:

| Project | Max cut | Understanding | Random | Δ vs random | Floor |
|---|---:|---:|---:|---:|---|
| Government | **50.0%** | 90.1% | 90.1% | 0 pp | Yes |
| Engineering | 45.3% | 96.1% | 96.1% | 0 pp | Yes |
| Science | 61.2% | 91.6% | 91.6% | 0 pp | Yes |
| Social | 20.0% | 94.7% | 94.7% | 0 pp | Yes |
| Lab | 40.9% | 85.9% | 85.9% | 0 pp | **No** |

**Investor Round 2:** Gov floor pass is real progress (was 88% @ 20% cut pre-fix). Still **not fundable** — 0 pp delta vs random on offline proxy; LLM judge stub ready but not exercised (no API key).

**Client Round 2:** Science/Gov exports still pilot-worthy at floor; random tie remains objection #1. LLM judge + manifest per chunk before production embed.

---

## Actions out of meeting

| Owner | Action |
|---|---|
| CTO | Shipped `datter/eval/relevance_boost.py`; wired into SelectAgent; Executive tab floor warning |
| Research | P0: beat random on gov + lab with M2/M3; tune Lab eval questions |
| CFO | Lead Loom with Gov 50% cut + Science 61%; disclaimer on proxy |
| CEO | Round 2 review after production-judge spike |

## Links

- [[Multi-Model Review Loop]]
- [[Business Model & Finance]]
- [[Executive Finance Report]]
- [[HANDOFF]]
