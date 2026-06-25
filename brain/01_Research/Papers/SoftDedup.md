---
type: paper
status: skimmed
created: 2026-06-25
updated: 2026-06-25
title: "SoftDedup: an Efficient Data Reweighting Method for Speeding Up Language Model Pre-training"
authors:
  - Nan He
  - Weichen Xiong
  - Hanwen Liu
  - Yi Liao
  - Lei Ding
  - Kai Zhang
  - Guohua Tang
  - Xiao Han
  - Wei Yang
year: 2024
venue: arXiv
arxiv: "2407.06654"
doi: "10.48550/arXiv.2407.06654"
url: "https://arxiv.org/abs/2407.06654"
source_pdf: definition_pending
tags:
  - paper
  - deduplication
  - data-reweighting
  - pretraining
projects:
  - datter
read_depth: skim
confidence: medium
agent_access: default
aliases:
  - Soft Dedup
---

# SoftDedup

## One-line thesis

Duplicated or common data can be downweighted instead of removed, preserving dataset integrity while improving training efficiency.

## Why it matters to Datter

Datter should not only recommend "drop." A stronger product can recommend keep, compress, review, or downweight depending on usefulness and redundancy.

## Problem

Hard deduplication can remove useful information and does not capture degrees of duplication.

## Method (5 bullets max)

- Define data commonness as a degree-of-duplication signal.
- Estimate commonness using n-gram occurrence probabilities.
- Reduce sampling weight for high-commonness data.
- Keep the data in the dataset rather than hard deleting it.
- Evaluate language-model pretraining efficiency and downstream few-shot accuracy.

## Key results (5 bullets max)

- The abstract reports comparable perplexity with at least 26 percent fewer training steps.
- It reports a 1.77 percent average few-shot downstream accuracy improvement for equal training duration.
- The method is reported to help even after rigorous deduplication.

## Limitations

- Abstract-level note only.
- Reweighting is pretraining-oriented; Datter's initial product is document-ingestion oriented.
- Needs full read before deciding how to compute commonness for mixed document collections.

## Datter implications

- Consider whether `recommended_action` should include "downweight" or whether "compress" is enough for MVP.
- Test whether hard drops remove useful repeated context in demo data.

## Mechanisms / equations worth remembering

- Data commonness.
- N-gram occurrence probability as a duplication-degree proxy.
- Sampling weight as an intervention.

## Quotes or numbers to cite

- arXiv: `2407.06654`
- Abstract numbers: at least 26 percent fewer training steps; 1.77 percent few-shot accuracy improvement.

## Related papers

- [[Deduplicating Training Data Makes Language Models Better]]
- [[SemDeDup]]
- [[ZIP-FIT]]

## Open questions

- Should Datter's first version output a reweighting recommendation rather than deletion?
- Can commonness be computed cheaply over local PDF/markdown/text folders?

## Links

- Up: [[Papers Map]]
- Experiments: [[Experiment Map]]
- Source: https://arxiv.org/abs/2407.06654

