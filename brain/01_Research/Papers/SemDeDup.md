---
type: paper
status: skimmed
created: 2026-06-25
updated: 2026-06-25
title: "SemDeDup: Data-efficient learning at web-scale through semantic deduplication"
authors:
  - Amro Abbas
  - Kushal Tirumala
  - Daniel Simig
  - Surya Ganguli
  - Ari S. Morcos
year: 2023
venue: arXiv
arxiv: "2303.09540"
doi: "10.48550/arXiv.2303.09540"
url: "https://arxiv.org/abs/2303.09540"
source_pdf: definition_pending
tags:
  - paper
  - semantic-deduplication
  - embeddings
  - data-curation
projects:
  - datter
read_depth: skim
confidence: medium
agent_access: default
aliases:
  - Semantic Deduplication
  - SemDeDup tradition
---

# SemDeDup

## One-line thesis

Embedding-based semantic duplicate removal can reduce web-scale training data while preserving performance and improving efficiency.

## Why it matters to Datter

This is the semantic-dedup baseline Datter will be compared against if it claims to find redundant or low-value data.

## Problem

Web-scale datasets contain semantic duplicates that exact deduplication misses.

## Method (5 bullets max)

- Use embeddings from pretrained models.
- Identify semantically similar data pairs.
- Remove semantic duplicates rather than only exact duplicates.
- Analyze image-text data and language-model data.
- Measure learning speed and performance after data removal.

## Key results (5 bullets max)

- The abstract reports removing 50 percent of a LAION subset with minimal performance loss.
- It reports effectively halving training time in that setting.
- It reports out-of-distribution performance increases.
- It reports efficiency gains on C4 language-model analysis.

## Limitations

- Abstract-level note only.
- Requires embeddings, whereas Datter may want a cheaper pre-embedding signal.
- Removing semantic duplicates is not the same as estimating economic usefulness.

## Datter implications

- Important baseline and competitor framing for duplicate/near-duplicate reduction.
- Decide whether embedding-based dedup is worth the extra cost in Datter MVP.

## Mechanisms / equations worth remembering

- Embedding similarity.
- Semantic duplicate pairs.
- Dataset reduction with performance-preservation checks.

## Quotes or numbers to cite

- arXiv: `2303.09540`
- Abstract claim: 50 percent data removal on a LAION subset with minimal performance loss.

## Related papers

- [[Deduplicating Training Data Makes Language Models Better]]
- [[SoftDedup]]
- [[ZIP-FIT]]

## Open questions

- Should Datter benchmark against exact dedup, semantic dedup, and compression selection separately?
- Can compression-based selection beat or complement embedding-based deduplication?

## Links

- Up: [[Papers Map]]
- Experiments: [[Experiment Map]]
- Source: https://arxiv.org/abs/2303.09540

