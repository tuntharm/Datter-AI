<div align="center">

  <img src="docs/assets/wordmark.png" alt="Datter.ai" width="420" />

  <p><strong>The input gate before embedding spend.</strong></p>

  <p>
    Upload a corpus → audit redundancy → select a smaller corpus → test it against your quality floor —
    <em>before</em> you pay for embeddings, inference, or training.
  </p>

  <p>
    <a href="https://github.com/tuntharm/Datter-AI"><img src="https://img.shields.io/badge/Python-3.10%2B-blue" alt="Python 3.10+" /></a>
    <a href="https://github.com/tuntharm/Datter-AI"><img src="https://img.shields.io/badge/Streamlit-local%20app-FF4B4B" alt="Streamlit" /></a>
    <a href="https://github.com/tuntharm/Datter-AI/actions/workflows/ci.yml"><img src="https://github.com/tuntharm/Datter-AI/actions/workflows/ci.yml/badge.svg" alt="CI" /></a>
    <a href="HACKATHON.md"><img src="https://img.shields.io/badge/hackathon-Cursor%20Hands%20Off%202026-8B5CF6" alt="Hackathon" /></a>
  </p>

</div>

---

## Meet Datter

<p align="center">
  <img src="docs/assets/brain-icon.png" alt="Datter brain mark" width="96" />
</p>

**Datter.ai** estimates how much of an AI corpus can be removed while keeping task-specific evaluation above a chosen quality floor.

Most teams pay to embed, label, fine-tune, or train on everything. A large share is redundant, near-duplicate, or low-signal. Datter audits the corpus first, selects a minimum-sufficient subset under a token budget, and exports an optimised corpus with an audit trail — so you only spend on data that still answers the questions that matter.

Built for RAG teams, ML engineers, and document-heavy orgs who need **proof**, not just a compression ratio.

---

## Dashboard at a glance

<p align="center">
  <img src="docs/assets/dashboard-demo.png" alt="Datter.ai dashboard — compression, quality retained, and ROI panels" width="920" />
</p>

<p align="center"><em>The evaluated Government sample shows the export reduction, offline quality proxy, and projected cost from one reproducible run.</em></p>

| Panel | What it shows |
| --- | --- |
| **A · Compression** | Estimated token cut and before/after token count |
| **B · Quality retained** | Q&A understanding at that cut (eval harness) or structural proxy when no queries are attached |
| **C · ROI / savings** | Avoidable embedding spend identified from your cost assumptions |

Tabs underneath cover **Proof** (per-question scores), **Export** (optimised `.zip`), **Executive** (business model), and **Audit** (pipeline log + chunk table).

---

## What it does

- **Upload-first** — drag PDF, TXT, or MD files; the pipeline scans automatically
- **7 automated stages** — Ingest → Chunk → Dedup → Score → Select → Eval → Report
- **Task-conditioned selection** — relevance boost from `queries.json` when you define downstream questions
- **Proof loop** — offline TF-IDF retrieval + token-overlap judge (or LLM judge when API keys are set)
- **Optimised export** — `.zip` of selected `.txt` chunks + `manifest.json`, plus Markdown/JSON audit reports
- **Sample corpora** — Government, Social, Engineering, Science, and a fast Lab dataset for demos

> **One-line pitch:** Datter estimates how much of an AI corpus can be removed while keeping task-specific evaluation above your quality floor — before you spend on embeddings, inference, or training.

---

## Product status

| Area | Status | Notes |
| --- | --- | --- |
| Upload + auto-scan | **Working** | Streamlit hands-off flow |
| Structural audit (dedup, density, cost) | **Working** | Baseline heuristic scorer |
| Token-budget selection | **Working** | Datter cut vs random at budget |
| Proof loop (`queries.json`) | **Working** | Offline proxy; LLM judge optional |
| Known-demo PDF auto-match | **Working** | Re-uploaded sample PDFs wire eval automatically |
| Optimised corpus export | **Working** | Zip + manifest |
| Adisorn complexity model | **Planned** | Plugin slot exists; model files not bundled |
| S3 / SQL / Kafka connectors | **UI placeholder** | Shown as coming soon |
| Auth, billing, multi-tenant | **Out of scope (MVP)** | Local-first hackathon build |

### Example proof result (Government sample)

On `managing_public_money.pdf` with Treasury compliance questions:

| Metric | Value |
| --- | --- |
| Evaluation target | **50% token reduction** |
| Q&A proxy retained | **90.1%** |
| Quality floor | **90%** |
| Judge | TF-IDF retrieval + token-overlap proxy |

*Demo disclaimer: this is an illustrative offline proxy, not a production benchmark. Production claims require representative client queries and a validated evaluation harness.*

---

## How it works

```mermaid
flowchart LR
    A[Upload PDF / TXT / MD] --> B[Ingest + chunk]
    B --> C[Dedup exact + near-dup]
    C --> D[Score density + redundancy]
    D --> E[Select under token budget]
    E --> F{queries.json?}
    F -->|yes| G[Proof loop @ quality floor]
    F -->|no| H[Structural proxy only]
    G --> I[Report + export zip]
    H --> I
```

**Selection engine** is the core: score chunks for marginal value, pack the highest-signal set into a token budget, then verify (or estimate) that downstream Q&A understanding still clears your floor.

---

## Try sample corpora

Use the sidebar **Try sample** buttons, or upload a file that matches a known demo PDF (filename or byte fingerprint).

| Project | Corpus | Eval questions |
| --- | --- | --- |
| **Government** | `managing_public_money.pdf` | Treasury compliance RAG |
| **Social** | `who_social_connection.pdf` | WHO social-connection policy |
| **Engineering** | `nist_seismic_smf_guide.pdf` | NIST seismic design guide |
| **Science** | `plos_climber_x_paleoclimate.pdf` | PLOS paleoclimate paper |
| **Lab** | `demo_data/` mixed files | Fast structural audit (~2s) |

Each vertical ships with `queries.json` and a pre-run `eval_cache.json` for instant proof-loop metrics.

---

## Quick start

### Prerequisites

- Python 3.10 or newer

### Install and run

```bash
git clone https://github.com/tuntharm/Datter-AI.git
cd Datter-AI

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

streamlit run app.py
```

Open [http://127.0.0.1:8501](http://127.0.0.1:8501).

**Fastest demo:** sidebar → **Try sample → Government** or upload `demo_verticals/government/managing_public_money.pdf`.

### Tests

```bash
pytest tests/ -q
```

---

## Repository layout

```text
Datter-AI/
├── app.py                      # Streamlit dashboard (upload gate + outcome panels)
├── assets/brand/               # Brain icon + wordmark (also in docs/assets for README)
├── docs/assets/                # README screenshots and brand images
├── datter/
│   ├── agent.py                # Seven-stage streaming pipeline
│   ├── project.py              # Sample projects + upload→sample matching
│   ├── selection.py            # Token-budget cut + query relevance boost
│   ├── export.py               # Optimised corpus zip export
│   ├── eval/                   # Offline proof loop, Pareto floor, paper-summary team
│   └── scorers/                # Baseline / Adisorn / hybrid plugin interface
├── demo_verticals/             # Government, Social, Engineering, Science PDFs + queries
├── demo_data/                  # Fast lab corpus
├── scripts/                    # Compression ladder, paper-summary team runners
├── tests/                      # 30 pytest tests
├── HACKATHON.md                # Demo script for judges / Loom
└── AGENTS.md                   # Contributor routing for humans + agents
```

---

## Scoring engines

| Mode | Description |
| --- | --- |
| **Baseline** | Heuristic redundancy, novelty, density + gzip complexity proxy |
| **Adisorn** | Wrapper for Adisorn Panasawatwong's complexity model (placeholder until model files added) |
| **Hybrid** | Blends baseline + Adisorn when the research model is loaded |

See [`models/adisorn/README.md`](models/adisorn/README.md) for model integration notes.

---

## Research grounding

Baseline signals are informed by recent data-compression and selection literature:

| Paper | Insight for Datter |
| --- | --- |
| [Kim & Baek 2024](https://arxiv.org/abs/2406.14124) | Entropy-based sample importance; low-info samples are pruning candidates |
| [ZIP-FIT 2024](https://arxiv.org/abs/2410.18194) | Gzip NCD for task-aligned selection |
| [PreSelect 2025](https://proceedings.mlr.press/v267/shum25a.html) | Compression efficiency predicts downstream value |
| [SoftDedup 2024](https://arxiv.org/abs/2407.06654) | Reweight vs hard-drop for near-duplicates |

---

## 60-second demo script

1. *"AI teams pay to process everything — most of it is redundant."*
2. Upload a PDF or click **Try sample → Government** — watch the pipeline log on the left.
3. Point to **estimated cut**, **quality retained**, and **avoidable embedding spend**.
4. Open **Proof** — show per-question scores at the cut.
5. Download the optimised corpus zip.
6. *"Datter.ai — test which data still matters before paying to process all of it."*

Full judge script: [`HACKATHON.md`](HACKATHON.md).

---

## Feedback

Feedback and issues are welcome, especially around evaluation quality, selection methods, and representative demo corpora.

The repository is source-available but not currently open source. Please do not reuse or redistribute the code without permission.

---

## License

No open-source license has been selected yet. Unless a license file is added, the repository is publicly viewable but all rights remain reserved.

---

<div align="center">

  <img src="docs/assets/brain-icon.png" alt="Datter.ai" width="48" />

  <p><strong>Datter.ai</strong> — the input gate before embedding spend.</p>

  <p>
    <a href="https://github.com/tuntharm/Datter-AI">GitHub</a>
    ·
    Built for <a href="HACKATHON.md">Cursor Hands Off London 2026</a>
  </p>

</div>
