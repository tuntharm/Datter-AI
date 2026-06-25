# Demo Dataset

One-click demo for Datter AI Hands-Off. Expected outcomes:

| File | Purpose | Expected action |
|------|---------|-----------------|
| `01_unique_research_note.md` | High-value unique research content | **keep** |
| `02_near_duplicate_of_01.md` | Paraphrased overlap with 01 | **compress** / **review** |
| `03_exact_duplicate_of_01.txt` | Verbatim copy of 01 | **drop** |
| `04_boilerplate_policy.md` | Legal boilerplate, low density | **drop** / **compress** |
| `05_dense_technical_spec.pdf` | Dense unique technical content | **keep** |
| `06_low_signal_meeting_notes.txt` | Filler meeting notes | **review** / **drop** |

Target: **30–50% avoidable tokens** on the bundled set.
