---
type: product
status: active
created: 2026-06-25
updated: 2026-06-25
tags:
  - product
  - gtm
  - investor
source: orchestration-integrator-2026-06-25
---

# Investor Outreach Brief — 1 page

**For:** Business team reaching pre-seed / seed AI infra and dev-tools investors.  
**Demo link:** local Streamlit (`streamlit run app.py`) — Executive tab = economics.

---

## One-liner

Datter finds the **maximum token cut** that preserves a customer-chosen **quality floor** on their eval questions — proven vs random at the same budget, with an audit trail.

## Problem

RAG teams embed entire PDF corpora ($27k storage → $150k labeling → $400k+ GPU) without knowing which tokens actually support their bot. Dedup tools remove obvious waste but don't optimise for **task understanding**.

## Product (live tonight)

| Proof point | Number | Project |
|---|---:|---|
| Best max safe cut @ 90% floor | **61.2%** | Science PDF |
| Regulated-style handbook | **50.0% cut, 90.1% understanding** | Government PDF |
| Hands-off pipeline | 7 agents, zero clicks | All projects |

**Honest limit:** Offline TF-IDF proxy — not production LLM judge. Datter **meets floor on 4/4 vertical PDFs** after Round 1 selector fix; **ties random** on delta (Round 2 target: beat random + LLM judge).

## Moat thesis

1. **Project-scoped eval harness** — quality floor is contractual, not guessed.
2. **Pareto scan SKU** — max cut @ floor, not fixed 50% for everyone.
3. **Research flywheel** — better scorers move frontier (Round 1: gov 20%→50% max cut from query relevance alone).

## Business model

Price per **M tokens analysed** or per **project**, tiered by floor: Standard 90%, Assured 95%, Governed 99%. See [[Business Model & Finance]].

## Ask

**Seed / pre-seed:** $1.5–2.5M to (1) production LLM judge + design-partner pilots, (2) M2/M3 selector research, (3) first 5 paying RAG teams.

## Do / Don't in first email

| Do | Don't |
|---|---|
| Lead with input-gate ROI + max cut @ floor | Claim absolute "92% accuracy" |
| Offer 15-min demo + Gov/Science tabs | Promise universal beat-random without disclaimer |
| Link [[CEO Pitch Meeting 2026-06-25]] | Lead with datacenter or training-accuracy pitch |

## Next meeting agenda (30 min)

1. Live demo — Government Executive tab (50% cut @ 90.1%)
2. Proof limitations + Round 2 roadmap (LLM judge, beat random)
3. Design partner offer — one corpus, scoped eval, 2-week pilot

## Links

- [[Business Outreach Brief]]
- [[CEO Review Meeting 2026-06-25]]
- [[Executive Finance Report]]
