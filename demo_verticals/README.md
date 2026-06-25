# Demo verticals — proof corpus

Download PDFs from [Vertical Demo Corpus](brain/02_Product/Orchestration/Vertical%20Demo%20Corpus.md).

```text
demo_verticals/
  government/   managing_public_money.pdf + queries.json + eval_cache.json
  social/       who_social_connection.pdf + queries.json + eval_cache.json
  engineering/  nist_seismic_smf_guide.pdf + queries.json + eval_cache.json
  science/      plos_climber_x_paleoclimate.pdf + queries.json + eval_cache.json
```

**Lab project:** `demo_data/` (structural audit bundle with strong savings signal).

One **project** = one folder + `queries.json` + eval cache. Do not mix verticals in a single score run.

Run: `streamlit run app.py` — pick project, agents auto-run.
