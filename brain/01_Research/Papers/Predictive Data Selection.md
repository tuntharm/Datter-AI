---
type: paper
status: skimmed
created: 2026-06-25
updated: 2026-06-25
title: "Predictive Data Selection: The Data That Predicts Is the Data That Teaches"
authors:
  - Kashun Shum
  - Yuzhen Huang
  - Hongjian Zou
  - Qi Ding
  - Yixuan Liao
  - Xiaoxin Chen
  - Qian Liu
  - Junxian He
year: 2025
venue: ICML 2025
arxiv: "2503.00808"
doi: "10.48550/arXiv.2503.00808"
url: "https://arxiv.org/abs/2503.00808"
source_pdf: definition_pending
tags:
  - paper
  - data-selection
  - pretraining
projects:
  - datter
read_depth: skim
confidence: medium
agent_access: default
aliases:
  - PreSelect
  - The Data That Predicts Is the Data That Teaches
---

# Predictive Data Selection

## One-line thesis

Data whose model losses predict downstream ability is especially useful training data.

## Why it matters to Datter

Datter's core claim is that some data deserves AI spend and some does not. PreSelect gives a concrete version of that claim for pretraining: predictive data teaches better.

## Problem

Large pretraining corpora are expensive, and generic data-quality filters may not estimate which data actually contributes to learning.

## Method (5 bullets max)

- Start from the observation that compression efficiency can correlate with downstream performance when domains align.
- Treat predictiveness of model losses as a signal of data contribution.
- Train and deploy a fastText-based scorer.
- Select pretraining data using that scorer.
- Evaluate at 1B and 3B parameter scales.

## Key results (5 bullets max)

- The abstract reports that 30B selected tokens can beat a 300B-token vanilla baseline.
- It frames this as a 10x compute reduction.
- It reports outperformance over DCLM and FineWeb-Edu baselines in a 3B-model, 100B-token setting.
- The authors released a trained scorer and curated datasets.

## Limitations

- Abstract-level note only.
- Focused on pretraining; Datter's first wedge is pre-ingestion/token waste, so transfer needs testing.
- Needs full read before making strong compute-reduction claims.

## Datter implications

- Datter should eventually test whether its scores predict downstream retrieval or QA usefulness.
- Do not stop at token savings; validate no quality collapse.

## Mechanisms / equations worth remembering

- Predictive losses as a data-value signal.
- FastText-based scorer as a lightweight selection mechanism.

## Quotes or numbers to cite

- arXiv: `2503.00808`
- ICML 2025 according to arXiv comments.
- Abstract claim: 30B selected tokens outperform 300B-token vanilla baseline.

## Related papers

- [[ZIP-FIT]]
- [[Why Less is More Sometimes]]
- [[Measuring Sample Importance in Data Pruning]]

## Open questions

- Can a document-level Datter score predict downstream retrieval usefulness without training a model?
- What minimum evaluation would make this claim credible for a demo?

## Links

- Up: [[Papers Map]]
- Experiments: [[Experiment Map]]
- Source: https://arxiv.org/abs/2503.00808

