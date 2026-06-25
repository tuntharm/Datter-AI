---
type: paper
status: to_read
created: 2026-06-25
updated: 2026-06-25
title: "Measuring Sample Importance in Data Pruning for Language Models based on Information Entropy"
authors:
  - Minsang Kim
  - Seungjun Baek
year: 2024
venue: arXiv
arxiv: "2406.14124"
doi: "10.48550/arXiv.2406.14124"
url: "https://arxiv.org/abs/2406.14124"
source_pdf: definition_pending
tags:
  - paper
  - data-pruning
  - entropy
projects:
  - datter
read_depth: skim
confidence: medium
agent_access: default
aliases:
  - Measuring Sample Importance via Data Compression
  - Tan et al. 2024 sample importance
---

# Measuring Sample Importance in Data Pruning

## One-line thesis

Entropy-like sample informativeness signals can rank training examples so lower-information, more redundant samples are pruned first.

## Why it matters to Datter

Datter needs defensible ways to score which data is worth spending AI budget on before training or inference. This paper is relevant as a lightweight sample-value signal, but the old project label appears mismatched with the arXiv metadata.

## Problem

Language-model training corpora contain redundant or low-information samples, and pruning them without hurting downstream performance is hard.

## Method (5 bullets max)

- Rank samples by estimated informativeness.
- Use entropy functions as surrogates for sample importance.
- Include negative log-likelihood and average inverse word frequency signals.
- Prune less informative samples first.
- Evaluate language modeling and downstream task performance after pruning.

## Key results (5 bullets max)

- The abstract reports improved language-modeling and downstream-task behavior.
- The approach is framed as compute-efficient data pruning.
- The signal treats redundant data as lower priority for training.

## Limitations

- Seeded from public metadata and abstract only.
- The old project label called this "Tan et al. 2024" and "via Data Compression"; arXiv metadata lists Kim and Baek with an entropy framing.
- Need full read before citing exact metrics.

## Datter implications

- Candidate signal for a "learnable information" or redundancy score.
- Do not cite as a Tan/compression paper until the intended source is found.

## Mechanisms / equations worth remembering

- Entropy-based informativeness.
- Negative log-likelihood as a sample information proxy.
- Average inverse word frequency as a lightweight text signal.

## Quotes or numbers to cite

- arXiv: `2406.14124`
- Cite only after a full read because the seed label and source metadata disagree.

## Related papers

- [[ZIP-FIT]]
- [[Predictive Data Selection]]
- [[SoftDedup]]

## Open questions

- Is there a separate Tan et al. compression paper that the old Datter README intended?
- How well do entropy proxies transfer to pre-ingestion document triage?

## Links

- Up: [[Papers Map]]
- Experiments: [[Experiment Map]]
- Source: https://arxiv.org/abs/2406.14124

