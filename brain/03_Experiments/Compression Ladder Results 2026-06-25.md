---
type: experiment-result
status: complete
created: 2026-06-25
updated: 2026-06-25
tags:
  - experiment
  - compression
  - paper-summary-team
  - datter
---

# Compression Ladder Results 2026-06-25

**HANDOFF `[Paper Summary Team] Compression ladder sweep`** — Progressive ladder (10%→70%, stop below 90% quality floor) run with offline TF-IDF judge fallback across all five demo projects. Engineering and science were already complete; government, social, and lab were run 2026-06-25.

**Method:** `scripts/run_compression_ladder.py` · Judge: Paper Summary Team offline (TF-IDF retrieval + token overlap) · Floor: 90% min score across model roster.

## Max safe compression (all papers)

| Project | Paper / corpus | Max safe cut | Min score | Tokens saved |
|---------|----------------|-------------:|----------:|-------------:|
| Lab | Structural audit (mixed corpus) | — | 45.4% @ 96% cut | 0 |
| Government | *Managing Public Money* | 20.0% | 92.9% | 26,361 |
| Engineering | NIST Seismic SMF Guide | 40.0% | 96.1% | 13,936 |
| Science | CLIMBER-X paleoclimate (PLOS) | 40.3% | 94.4% | 8,910 |
| Social | WHO Social Connection report | 15.0% | 91.0% | 24,217 |

**Lab note:** At the 10% target, dedup/selection overshoots to 96% actual reduction and fails the floor on the first step — no rung passes. Lab is useful for structural-audit signal, not compression-at-floor claims.

## Artifacts

| Project | JSON | Summary |
|---------|------|---------|
| Lab | `demo_data/compression_ladder.json` | `demo_data/compression_ladder_summary.md` |
| Government | `demo_verticals/government/compression_ladder.json` | `demo_verticals/government/compression_ladder_summary.md` |
| Engineering | `demo_verticals/engineering/compression_ladder.json` | — |
| Science | `demo_verticals/science/compression_ladder.json` | — |
| Social | `demo_verticals/social/compression_ladder.json` | `demo_verticals/social/compression_ladder_summary.md` |

*Production claims require live multi-model Paper Summary Team run (API keys).*
