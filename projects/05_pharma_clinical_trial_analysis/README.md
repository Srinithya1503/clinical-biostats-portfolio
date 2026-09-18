# Pharma Pipeline and Clinical Trial Benchmarking Analysis - ClinicalTrials.gov - Oncology
---
## Description

A Pharma Pipeline and Clinical Trial Benchmarking Analysis is a market research and competitive intelligence framework used by pharma companies, CROs, and biotech consultancies. It evaluates where a drug, therapy, or company stands against competitors across clinical development stages (Phase 1–3), therapeutic areas, target indications, and mechanism of action (MoA).

---
## 1. Objective

To evaluate competitive density, identify white spaces (underserved indications), forecast clinical timeline risks, and benchmark drug performance metrics against market competitors.

---
## 2. About dataset

A few things worth knowing about `raw_trials.csv` before look at the results:

- **Extracted data using REST API** live clinical trial data from the ClinicalTrials.gov v2 REST API (https://clinicaltrials.gov/api/v2/studies) for a specified condition (e.g., "Non-Small Cell Lung Cancer" or "Oncology"),
- **819 of 2,000 trials (41%) have no phase listed** (`phase` is blank or `"NA"`/`"N/A"` in the source data) — both scripts group these under `"N/A"` rather than dropping them, so they still count toward the phase distribution, sponsor counts, and enrollment numbers, but not toward the duration averages' interpretation as a specific phase.
- **About 35% of `start_date` values only have a year and month** (e.g.`2007-04`, no day). Both scripts treat these as the 1st of that month rather than discarding them.
- **75 trials have no `completion_date`** (still ongoing) and are excluded only from the duration calculation, not from the other three metrics.
- **No duplicate `nct_id` values** were found in this file, so the duplicate-removal step has no effect here — it's kept in both scripts in
  case you re-run this on a newer, larger export where duplicates could appear.

---
## 3. Project Repository Structure
```
05_pharma_clinical_trial_analysis/
├── README.md
├── raw_trials.csv                  ← your uploaded file (2,000 trials)
├── clinical_trial_analysis.ipynb   ← Python notebook, already executed
├── sas_analysis_basic.sas          ← plain/basic SAS version
└── results/                        ← the 4 output CSVs, already generated
```

---
## 4. Analysis Methods
This package analyzes the uploaded raw clinical trial dataset (`raw_trials.csv`, 2,000 trials pulled from ClinicalTrials.gov) two ways:
1. **`clinical_trial_analysis.ipynb`** — a Jupyter notebook (Python / pandas), already run end-to-end against your file, with the real tables and charts
   saved inside it.
2. **`sas_analysis_basic.sas`** — the same analysis in plain, beginner-level SAS: only `PROC IMPORT`, `DATA` steps, `PROC SORT`, `PROC FREQ`, `PROC MEANS`,
   `PROC PRINT`, and `PROC EXPORT`.
Both do the same four things: clean the raw data, then calculate phase distribution, top sponsors, median enrollment by phase, and trial duration by phase.

---
## 5. Results (from the executed Python notebook, on actual data)

**Phase distribution**

| Phase | Trial Count | % |
|---|---|---|
| N/A | 819 | 40.95% |
| PHASE2 | 551 | 27.55% |
| PHASE1 | 400 | 20.00% |
| PHASE3 | 161 | 8.05% |
| PHASE4 | 35 | 1.75% |
| EARLY_PHASE1 | 34 | 1.70% |

**Top 5 sponsors** (of the top 10 saved in `results/top_sponsors.csv`)

| Sponsor | Trial Count |
|---|---|
| National Cancer Institute (NCI) | 57 |
| M.D. Anderson Cancer Center | 40 |
| Memorial Sloan Kettering Cancer Center | 27 |
| Sun Yat-sen University | 24 |
| Novartis Pharmaceuticals | 23 |

**Median enrollment by phase:** Highest is PHASE3 at 302 patients, Lowest is EARLY_PHASE1 at 27.5 patients — enrollment size scales up clearly with later
trial phases, as expected.
**Trial duration by phase:** averages range from about 1,204 days (PHASE4) to about 2,057 days (PHASE3), with PHASE3 trials taking the longest on
average — consistent with PHASE3 trials being the largest, most enrollment-heavy studies.

---
## 5. Notes / assumptions

- "Top sponsors" is fixed at the top 10 in both scripts. To change it, edit `.head(10)` in the notebook or `(obs=10)` in the SAS script.
- Duration is `completion_date − start_date` in days. Rows with a missing or negative duration are excluded only from that specific metric.
- The SAS script intentionally avoids macros and `PROC SQL` so it's easy to read top-to-bottom for anyone still learning SAS — if you'd like a version
  using macros, arrays, or `PROC SQL` joins instead, that's a quick follow-up.

---


