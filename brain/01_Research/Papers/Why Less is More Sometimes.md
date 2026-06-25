---
type: paper
status: to_read
created: 2026-06-25
updated: 2026-06-25
title: "Why Less is More (Sometimes): A Theory of Data Curation"
authors:
  - Elvis Dohmatob
  - Mohammad Pezeshki
  - Reyhane Askari-Hemmat
year: 2025
venue: arXiv
arxiv: "2511.03492"
doi: "10.48550/arXiv.2511.03492"
url: "https://arxiv.org/abs/2511.03492"
source_pdf: definition_pending
tags:
  - paper
  - data-curation
  - theory
  - scaling-laws
projects:
  - datter
read_depth: skim
confidence: medium
agent_access: default
aliases:
  - Why Less is More
  - Theory of Data Curation
---

# Why Less is More Sometimes

## One-line thesis

Curated subsets can outperform full datasets under specific data-quality, difficulty, and oracle-noise conditions.

## Why it matters to Datter

Datter needs a theory story behind "less data can be better." This paper may supply conditions for when that claim is true rather than slogan-level.

## Problem

Classical scaling intuition says more data is better, but curated small datasets sometimes beat larger datasets.

## Method (5 bullets max)

- Study data curation using an imperfect oracle.
- Model selection by difficulty and correctness.
- Derive scaling-law curves for test error.
- Compare label-agnostic and label-aware curation.
- Validate theoretical predictions empirically on ImageNet.

## Key results (5 bullets max)

- The abstract reports phase-transition conditions where curation improves generalization.
- It argues small curated datasets can outperform full datasets under certain conditions.
- It connects the theory to recent LLM mathematical-reasoning curation strategies.

## Limitations

- Abstract-level note only.
- Theory assumptions must be checked before using this in product claims.
- ImageNet validation may not transfer directly to enterprise-document or RAG settings.

## Datter implications

- Use as a caution: "less is more" is conditional, not universal.
- Convert assumptions into Datter validation cases.

## Mechanisms / equations worth remembering

- Imperfect oracle selection.
- Difficulty and correctness dimensions.
- Phase-transition curves for when curation helps.

## Quotes or numbers to cite

- arXiv: `2511.03492`
- Do not cite exact theorem claims until full read.

## Related papers

- [[Predictive Data Selection]]
- [[ZIP-FIT]]
- [[Understanding LLM Behaviors via Compression]]

## Open questions

- What assumptions map to Datter's pre-ingestion scoring?
- Can Datter estimate an oracle-like usefulness signal without labels?

## Links

- Up: [[Papers Map]]
- Experiments: [[Experiment Map]]
- Source: https://arxiv.org/abs/2511.03492

