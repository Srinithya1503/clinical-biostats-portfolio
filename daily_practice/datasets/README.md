# ONCO-2026: Synthetic Oncology Phase III RCT Dataset

## About This Dataset

ONCO-2026 is a fully synthetic, multi-domain clinical trial database simulating a **Phase III, double-blind, 1:1 randomized controlled trial** of Experimental 
Drug X versus Placebo in 500 solid tumor patients across 15 international sites.

Every file is modelled after real Electronic Data Capture (EDC) system exports — the kind a SAS programmer or biostatistician would receive at a CRO or pharma 
company on Day 1 of a project. The dataset is deliberately imperfect: it contains missing values, duplicate records, outlier lab results, ongoing adverse 
events with no end date, and protocol deviations — because real trial data always does.

---

## Study Design at a Glance

- **Phase:** III
- **Blinding:** Double-blind
- **Randomization:** 1:1 stratified by site
- **Treatment Arms:** ARM A = Experimental Drug X · ARM B = Placebo
- **Population:** Solid tumor patients aged 18–85
- **Sites:** 15 sites across USA, UK, Germany, France, Japan, Canada, 
  Australia, Italy, Spain, Netherlands, Belgium, Switzerland
- **Study Duration:** 24 months
- **Primary Endpoint:** Overall Survival (OS)
- **Secondary Endpoints:** Objective Response Rate (ORR), 
  Disease Control Rate (DCR), Safety & Tolerability

---

## What Makes This Dataset Realistic

**Embedded statistical signal**
ARM A genuinely outperforms ARM B — median OS ~480 vs ~360 days, 
higher tumor response rates, more treatment-related AEs. Your analyses 
will return clinically meaningful results, not noise.

**Real-world data quality issues (intentional)**
- 3–5% missing demographics and lab values
- ~0.5% duplicate lab records (simulating EDC extract bugs)
- ~1% outlier lab values (2.5–4× the normal result)
- ~10% of AE end dates missing (ongoing events)
- ~8% of lab visits entirely skipped
- Inconsistent follow-up lengths across subjects
- Protocol deviations affecting ~60% of subjects

**Longitudinal structure**
One subject can have 50+ rows across all domains — exactly the 
one-to-many relationships that make clinical data challenging to work with.

---

## CDISC SDTM Domain Mapping

| Raw File | → | SDTM Domain | ADaM Dataset |
|---|---|---|---|
| raw_dm.csv | → | DM + EX | ADSL |
| raw_lab.csv | → | LB | ADLB |
| raw_ae.csv | → | AE | ADAE |
| raw_cm.csv | → | CM | — |
| raw_vitals.csv | → | VS | ADVS |
| raw_tumor.csv | → | TU + RS | ADRS |
| raw_survival.csv | → | DS | ADTTE |
| raw_pd.csv | → | DV | — |

---

## Suggested Analysis Exercises

**Beginner**
- Merge all domains on SUBJID and profile the study population
- Count AEs by severity and treatment arm
- Plot vital signs over time

**Intermediate**
- Build a Demographics Summary Table (Table 14.1.1 format)
- Calculate Objective Response Rate with 95% Wilson CI by arm
- Produce a waterfall plot of % change in tumor size

**Advanced**
- Kaplan-Meier OS curves with log-rank test and median OS with 95% CI
- Multivariate Cox proportional hazards model adjusted for age, sex, and baseline tumor size
- Build ADSL from scratch following CDISC ADaM IG
- Create a shift table for lab abnormalities (baseline → worst on-study)
- Forest plot of subgroup OS hazard ratios

---

## Data Dictionary

A full data dictionary is included as `ONCO2026_DataDictionary.xlsx` with:
- Variable name, type, label, and description
- Example values
- CDISC SDTM variable mapping for every column
- Covers all 8 raw domains across 9 Excel tabs

---
### `ONCO2026_DataDictionary.xlsx` — Data Dictionary
> 9-tab Excel workbook. Summary tab lists all datasets with row counts. Each subsequent tab covers one domain with variable name, data type, label, description, example values, and CDISC SDTM mapping column.

### `ONCO2026_CDISC_Mapping.csv` — CDISC Crosswalk
| Column | Description |
|---|---|
| Raw Dataset | Source CSV filename |
| Raw Variable | Variable name in the raw file |
| CDISC Domain | Target SDTM domain (DM, LB, AE, CM, VS, TU, RS, DS, DV) |
| SDTM Variable | Target SDTM variable name |
| Notes | Transformation notes (ISO 8601 dates, controlled terminology, derivations) |

---

## Who Is This For?

| Role | What to Practice |
|---|---|
| **SAS Clinical Programmer** | PROC IMPORT, PROC SORT, PROC MEANS, ADSL/ADTTE/ADLB derivation, TLF shells |
| **Biostatistician** | Kaplan-Meier, Cox regression, logistic regression, mixed models, ORR/DCR |
| **CDISC/SDTM Mapper** | DM, LB, AE, CM, VS, TU, RS, DV domain creation |
| **R Programmer** | tidyverse, survival, ggplot2, gtsummary, forestplot |
| **Python Analyst** | pandas, lifelines, matplotlib, seaborn, scikit-learn |
| **Data Engineer** | Multi-table joins, longitudinal reshaping, data quality pipelines |

---

## License

**CC0 1.0 — Public Domain**
Use freely for education, research, portfolio projects, or teaching. 
No attribution required, though always appreciated.

---

## Disclaimer

> This dataset is **entirely synthetic**. It was generated programmatically 
> using Python (NumPy, Pandas) with no connection to any real clinical trial, 
> patient, institution, or pharmaceutical compound. It does not represent 
> the results of any actual study and should not be used for any medical, 
> regulatory, or clinical decision-making purpose.
