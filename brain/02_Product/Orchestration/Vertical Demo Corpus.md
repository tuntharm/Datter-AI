---
type: product
status: active
created: 2026-06-25
updated: 2026-06-25
tags:
  - product
  - demo
  - corpus
source: ceo-chat-2026-06-25
---

# Vertical Demo Corpus

Real-world PDFs for proof demo — **not** the 8 ML paper notes in `brain/01_Research/Papers/` (those inform scoring research only).

Tharm downloads PDFs manually; place under `demo_verticals/`. App already ingests `.pdf` via upload or folder path.

## Folder layout (target)

```text
demo_verticals/
  government/
    managing_public_money.pdf    # or landlords_right_to_rent.pdf
    queries.json                 # TODO: 6–8 eval questions
  social/
    un_world_social_report_2025.pdf
    queries.json
  engineering/
    nist_seismic_smf_guide.pdf
    queries.json
  science/
    plos_climber_x_paleoclimate.pdf
    queries.json
```

Keep existing `demo_data/` for quick structural audit (~41% avoidable).

## Download links

### Government

| Doc | PDF | Licence |
|---|---|---|
| **Recommended** Managing Public Money (Apr 2026) | [PDF](https://assets.publishing.service.gov.uk/media/69e0b17861d2e8e9b9e42e13/Managing_Public_Money_-_April_2026.pdf) | Open Government Licence v3.0 |
| Alt (shorter) Landlords Right to Rent (Jun 2025) | [PDF](https://assets.publishing.service.gov.uk/media/6878ea540263c35f52e4dd75/270625_Landlords_guide_to_Right_To_Rent_Checks-.pdf) | GOV.UK |

Landing: [GOV.UK Managing Public Money](https://www.gov.uk/government/publications/managing-public-money)

### Social

| Doc | PDF |
|---|---|
| **Recommended** UN World Social Report 2025 | [PDF](https://desapublications.un.org/sites/default/files/publications/2025-04/250422%20BLS25022%20UDS%20UN%20World%20Social%20Report%20WEB.pdf) |
| Alt WHO Social Connection report | [PDF](https://iris.who.int/server/api/core/bitstreams/f5f60bc8-344b-4216-aa1a-fb22d57ad6e8/content) (CC BY-NC-SA 3.0 IGO) |

### Engineering

| Doc | PDF |
|---|---|
| **Recommended** NIST Seismic Design — Steel Special Moment Frames (2nd ed.) | [PDF](https://nvlpubs.nist.gov/nistpubs/gcr/2016/nist.gcr.16-917-41.pdf) |
| Alt NIST AMS 300-12 UUIDs in Product Data (2024) | [PDF](https://nvlpubs.nist.gov/nistpubs/ams/NIST.AMS.300-12.pdf) |

DOI: [10.6028/NIST.GCR.16-917-41](https://doi.org/10.6028/NIST.GCR.16-917-41)

### Science

| Doc | PDF | Licence |
|---|---|---|
| **Recommended** PLOS ONE — CLIMBER-X paleoclimate (2024) | [PDF](https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0300138&type=printable) | CC BY 4.0 |
| Alt PLOS Climate — African ape sites (2024) | [PDF](https://journals.plos.org/plimate/article/file?id=10.1371%2Fjournal.pclm.0000345&type=printable) | CC BY 4.0 |

## Size tip

Gov *Managing Public Money* and UN WSR 2025 may be large. For tight hackathon API/time budget, use **Landlords Right to Rent** + **WHO Social Connection** for live demo; pre-run others.

## queries.json format (TODO per vertical)

```json
{
  "task_description": "Answer questions about this document for a RAG assistant.",
  "quality_floor": 0.90,
  "target_token_reduction": 0.50,
  "questions": [
    {"id": "q1", "query": "...", "gold_hint": "optional short answer for judge"}
  ]
}
```

## Links

- Up: [[Orchestration Plan]]
- Proof: [[Proof Loop Spec]]
