---
type: log
status: active
created: 2026-06-25
updated: 2026-06-25
tags:
  - paper
  - research
  - queue
  - datter
---

# Paper Queue

> [!todo] Current Focus
> Use these papers to sharpen Datter's claim: data usefulness should be assessed before token, embedding, label, retrieval, or training cost is committed.

> [!tip] Reading Rule
> Deep-read only when the paper changes a product claim, scoring method, experiment, pitch, or implementation decision.

> [!warning] Avoid
> Do not let this become PDF collecting. If a paper is not linked to a Datter question, park it.

## Current Priority Queue

| Order | Paper | Status | Why Now | Next Datter Action |
|---|---|---|---|---|
| 1 | [[ZIP-FIT]] | skimmed | Strongest compression-selection precedent | Prototype compression-alignment experiment |
| 2 | [[SoftDedup]] | skimmed | Current app already has compress/drop actions | Compare hard drop vs reweight/compress recommendations |
| 3 | [[Deduplicating Training Data Makes Language Models Better]] | skimmed | Foundational redundancy and memorization evidence | Add deduplication caveat to pitch/testing notes |
| 4 | [[SemDeDup]] | skimmed | Baseline comparison for semantic redundancy | Decide whether Datter needs embedding baseline |
| 5 | [[Predictive Data Selection]] | skimmed | Strong compute-reduction claim | Full-read before citing compute claims |
| 6 | [[Why Less is More Sometimes]] | to_read | Theory for curated subsets | Extract conditions where curation helps |
| 7 | [[Understanding LLM Behaviors via Compression]] | to_read | Mechanistic compression framing | Clarify usefulness vs compressibility |
| 8 | [[Measuring Sample Importance in Data Pruning]] | to_read | Entropy sample-importance signal | Reconcile source metadata before citation |

## To-read Backlog

| Paper | Why | Next Action |
|---|---|---|
| [[Why Less is More Sometimes]] | Formal curation theory may support Datter's pitch beyond heuristics | Read assumptions and limits |
| [[Understanding LLM Behaviors via Compression]] | Compression view may sharpen "learnable structure" language | Read mechanism sections |
| [[Measuring Sample Importance in Data Pruning]] | Relevant to sample-value scoring, but source metadata differs from old README label | Verify relation before citing |

## Skimmed / Needs Deep Read

| Paper | Current Understanding | Deep-read Trigger |
|---|---|---|
| [[ZIP-FIT]] | Compression can measure task alignment without embeddings | Before implementing compression alignment |
| [[Predictive Data Selection]] | Predictive losses can identify high-value pretraining data | Before citing compute-reduction claims |
| [[SoftDedup]] | Commonness-based reweighting can reduce training steps | Before using "soft dedup" in product language |
| [[Deduplicating Training Data Makes Language Models Better]] | Deduplication reduces memorization and can improve efficiency | Before privacy or memorization claims |
| [[SemDeDup]] | Embedding similarity can remove semantic duplicates with small loss | Before comparing against semantic dedup |

## Cited / Done

| Paper | Used Where | Notes |
|---|---|---|
| definition_pending | definition_pending | Promote here only after README, deck, docs, or implementation cites it |

## Parked For Later

| Paper | Why Parked | Review Trigger |
|---|---|---|
| definition_pending | definition_pending | definition_pending |

## Links

- Up: [[Papers Map]]
- Intake: [[Paper Intake Protocol]]
- Experiments: [[Experiment Map]]

