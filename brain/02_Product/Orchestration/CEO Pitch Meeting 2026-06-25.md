---
type: product
status: active
created: 2026-06-25
updated: 2026-06-25
tags:
  - product
  - pitch
  - ceo
  - hackathon
source: ceo-orchestration-2026-06-25
---

# CEO Pitch Meeting — 2026-06-25

**Audience:** Internal team (CTO, CPO, CFO, Research, business outreach)  
**Duration:** 10 minutes  
**Goal anchor:** Datter preserves the **same level of data for AI to understand** (quality floor) while **maximizing token drop**.

---

## 0:00–1:30 — Problem

> "Every AI team embedding a document corpus is prepaying waste."

**The chain compounds before anyone asks if the data is worth it:**

```text
Storage ($27k) → Labeling ($150k) → GPU / training ($400k+)
```

RAG teams ingest entire PDF libraries — handbooks, policies, papers — into vector stores. Much of it is duplicate, boilerplate, or irrelevant to the actual task. They pay twice: once to embed junk, again every time retrieval pulls it into context.

**The wrong question:** "Is the data clean?"  
**The right question:** "Is this data worth AI spend — at the quality bar my product needs?"

Nobody owns that decision today. Dedup tools delete bytes, not usefulness. MLOps watches training fail after the money is spent. **Datter sits at the input gate** — before tokens and embeddings compound.

**North star (locked):** drop the **maximum** tokens while preserving **100% understanding** on the customer's eval set. We approach that asymptotically via better selection and scoring — not blind deletion.

---

## 1:30–4:00 — Product: selection engine, max cut at quality floor

> "We are not a dashboard. We are a **selection engine**."

**What Datter is**

| Not this | This |
|---|---|
| File compression | Minimum-sufficient token subset for downstream AI |
| Fixed 50% cut for everyone | **Max safe cut** at **your** quality floor |
| Structural guess alone | Eval-proven cut scoped to corpus + task + questions |

**How it works (7 autonomous agents, hands-off)**

1. **Ingest → Chunk → Dedup → Score** — structural audit of the corpus  
2. **Select** — Pareto scan finds the **largest token reduction** that still meets the quality floor  
3. **Eval** — proves Datter cut vs random cut at the same token budget  
4. **Report + Export** — optimised corpus, audit trail, ROI summary  

**The SKU:** at quality floor **F%**, max safe reduction **XX%** — understanding **YY%** (random **ZZ%** at same budget).

```text
Quality (understanding %)
  100% |●  full corpus
       | \
       |  \  ← Datter frontier (improves with research)
       |   ●── max safe cut @ floor
  floor|························
       |        ● random cut (same tokens, worse quality)
       +──────────────────────── Token reduction %
            0%              XX%  ← what we maximise
```

**Customer picks the floor** (90% Standard, 95% Assured, 99% Governed). **We maximise the cut.** Research (Adisorn, M2 task-conditioned scoring, M3) pushes the frontier up-left — more tokens dropped, same accuracy.

**Project-scoped:** corpus + task + eval questions live in one project. No cross-project scoring. See [[Project Model]].

---

## 4:00–6:00 — Demo proof

> "Hands-off agents on real PDFs — proof tab shows we beat random at the same budget."

**Live demo path** (`streamlit run app.py`):

| Step | What to show | Time |
|---|---|---|
| Load | **Government** project — *Managing Public Money* PDF auto-runs | 0:15 |
| Pipeline | 7-step agent stepper streams live (hands-off badge) | 0:45 |
| Outcome | Understanding retained, avoidable tokens, $ saved | 0:30 |
| Proof | Full vs Datter vs random per eval question + disclaimer | 0:45 |
| Export | Optimised corpus zip + audit JSON | 0:15 |
| Executive | CFO ROI + max safe cut @ floor | 0:30 |

**Five projects:** Government, Social (WHO), Engineering (NIST), Science (PLOS), **Lab** (fast fallback — ~41% avoidable, strongest structural story).

**What we claim tonight (honest):**

- Autonomous agent pipeline on real corpora ✓  
- Max cut @ quality floor with Pareto scan ✓  
- Datter vs random at same token budget on Proof tab ✓  
- Audit export + executive ROI ✓  

**What we disclaim (required):**

- Understanding % uses **offline TF-IDF + token-overlap proxy**, not production LLM judge  
- On some large PDFs (e.g. gov), random may beat Datter on the proxy — use **Lab** for strongest relative win or explain proxy limits  
- Production proof = LLM answer + judge ([[Proof Loop Spec]])

**Hackathon hook:** "Set up the workflow, let go, come back to an audit + optimised corpus." That is the Hands-Off thesis judges want.

---

## 6:00–8:30 — Business model

> "You pick the quality floor. We find the max cut. Price follows the floor."

See [[Business Model & Finance]] and [[Executive Finance Report]].

| Tier | Quality floor | Buyer | Price unit |
|---|---|---|---|
| **Audit (wedge)** | Structural only | Hackathon / PLG | Free local |
| **Standard** | 90% understanding | RAG teams, support bots | $/M tokens analysed |
| **Assured** | 95% | Regulated internal KB | $/project/month |
| **Governed** | 99% | Banks, VPC | Enterprise + audit trail |

**Pitch line for buyers:**  
"We removed **XX%** of tokens. Your bot still answers **YY%** as well as the full corpus on your test questions. Random cut at the same size only scored **ZZ%**."

**Flywheel:** win project → prove max cut @ floor → export optimised corpus → reinvest in scorer/selector/judge → **higher XX% at same floor** → upsell tier.

**Finance metrics per project:**

- Max safe reduction % (the SKU, not raw avoidable %)  
- Meets floor? (understanding ≥ floor)  
- Frontier delta vs random  
- $ saved = removed tokens × blended $/M  

**Research hiring thesis:** hire when floor is met but max cut is low (selector/M3), or cut is high but floor missed (scorer/Adisorn). **Do not sell** when random beats Datter on eval — fix scorer first.

---

## 8:30–10:00 — Ask

### From the team tonight

| Role | Ask |
|---|---|
| **CTO** | Live demo stable on **Lab** + **Government**; Proof disclaimer visible; Executive tab shows max safe cut + meets floor |
| **CPO** | Outcome-first Loom — hero metrics before tables; sidebar collapsed for recording |
| **CFO** | Lead Loom with avoidable $ + max cut @ floor; quality-tier close |
| **Research** | Push max cut on gov PDF without dropping below floor (Adisorn/M3 when ready) |
| **Business** | Three outreach tracks tonight — see [[Business Outreach Brief]] |

### From investor review (needed before external pitch hardens)

1. **Credibility bar:** confirm offline proxy is framed correctly; what proof bar unlocks seed narrative (3 corpora + LLM judge?)  
2. **Pricing sanity:** $/M analysed vs $/project at 90/95/99 floors — comparable to RAG spend saved  
3. **Defensibility:** selection engine + eval harness + research flywheel vs "just dedup"  
4. **Use of funds:** research hires tied to frontier lift (max cut @ floor), not headcount for dashboard

### From CTO (blockers to clear)

1. **Gov PDF eval gap** — random may beat Datter on offline proxy; need Lab fallback or scorer fix before claiming universal win  
2. **Production judge** — LLM API key + harness wiring ([[Proof Loop Spec]]) for post-hackathon credibility  
3. **Adisorn off** — baseline scorer limits frontier; document when hybrid unlocks gov vertical  
4. **Demo latency** — gov first run ~1–3 min; ensure eval cache + Lab path for live podium  

### Close (30 seconds)

> "Datter AI Hands-Off is an autonomous selection-engine company. You pick how much understanding you need. We find the maximum token cut that preserves it — and we keep pushing that frontier. Tonight we prove the agents, the audit, and the economics. Let's win the room."

---

## Links

- [[Hackathon Win Strategy]]
- [[Business Model & Finance]]
- [[Executive Finance Report]]
- [[Business Outreach Brief]]
- [[Loom Script]]
- [[HANDOFF]]
