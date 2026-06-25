# Hackathon demo — Cursor Hands Off London 2026

**Product:** Datter AI Hands-Off  
**Video:** Loom: PASTE_URL_HERE

## Quick start

```bash
cd /Users/tharm/dev/datter
source .venv/bin/activate
streamlit run app.py
```

## How to demo

1. **Upload path (main story):** drag PDF/TXT/MD files into the upload zone — agents scan automatically
2. **Sample path (fast Loom):** sidebar → **Try sample → Lab** (~2s, strong savings signal)
3. Watch **Structural Scan** progress on the left
4. Results on the right: **Compression** → **Quality retained** → **ROI / savings**
5. Download optimised corpus (.zip) or audit report (.md)

## Sample projects (sidebar only)

| Project | Corpus | Purpose |
|---|---|---|
| Government | `managing_public_money.pdf` | Real public-sector PDF |
| Social | `who_social_connection.pdf` | WHO health policy |
| Engineering | `nist_seismic_smf_guide.pdf` | NIST seismic design |
| Science | `plos_climber_x_paleoclimate.pdf` | PLOS paleoclimate paper |
| Lab | `demo_data/` | Fast structural audit (~41% avoidable) |

## What this demo proves

- **7 autonomous agents:** Ingest → Chunk → Dedup → Score → Select → Eval → Report
- **Upload-first input gate** — measure density before embedding spend
- **Score + compression + $ savings** on one page (no tab hunting)
- **Optimised corpus export** (.zip) + audit (.md / .json)
- Baseline scorer only (Adisorn deferred)

## Honest limits

- Understanding % uses **offline TF-IDF proxy** on sample projects with `queries.json`
- Raw uploads run structural audit only (no eval unless queries provided)
- S3 / SQL / Kafka connectors shown as coming soon

## Tests

```bash
pytest tests/ -q
```

## Submit blurb

> Datter AI Hands-Off is the input gate before RAG embedding: upload a corpus, autonomous agents scan for redundancy, score information density, compress to an optimised export, and deliver an audit report with projected savings. Built for Cursor Hands Off London 2026.
