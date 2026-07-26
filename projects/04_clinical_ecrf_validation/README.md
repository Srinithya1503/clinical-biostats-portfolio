# Clinical eCRF Data Validation & Clinical Data Quality Analysis

**A portfolio project for aspiring Clinical Data Coordinators, Clinical Data Management (CDM) Associates, and Clinical Data Analysts.**

> **Disclaimer:** All data in this repository is 100% synthetic and was generated programmatically for educational and portfolio purposes only. No real patient, subject, or site data was used at any stage of this project.

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Clinical Data Management Overview](#2-clinical-data-management-overview)
3. [What is an eCRF?](#3-what-is-an-ecrf)
4. [Why Data Validation Matters](#4-why-data-validation-matters)
5. [Project Workflow](#5-project-workflow)
6. [Folder Structure](#6-folder-structure)
7. [Validation Rules](#7-validation-rules)
8. [Dataset Description](#8-dataset-description)
9. [Notebook Walkthrough](#9-notebook-walkthrough)
10. [Output Files](#10-output-files)
11. [Dashboard](#11-dashboard)
12. [Clinical Relevance](#12-clinical-relevance)
13. [Resume Highlights](#13-resume-highlights)
14. [Interview Questions](#14-interview-questions--answers)
15. [Future Improvements](#15-future-improvements)

---

## 1. Executive Summary

This project simulates a real-world **Clinical Data Management (CDM)** workflow, from raw electronic Case Report Form (eCRF) data collection through to data validation, discrepancy management, and final data quality reporting.

It was built to demonstrate the core, day-to-day skills expected of an **entry-level Clinical Data Coordinator / Clinical Data Analyst**:

- Reviewing raw clinical trial data for completeness and accuracy
- Applying protocol-defined validation (edit-check) rules
- Identifying and logging data discrepancies as formal queries
- Tracking query status and resolution through to database lock readiness
- Summarizing data quality using clear, non-technical KPIs
- Communicating findings through tables, charts, and a written report

The project uses a **synthetic dataset** modeled on a small Phase II/III-style clinical trial:

| Attribute | Value |
|---|---|
| Subjects | 300 |
| Investigational Sites | 5 (SITE001–SITE005) |
| Scheduled Visits | 3 (Screening, Baseline, Week 4) |
| Raw eCRF Records | ~900 rows |
| Data Queries Logged | ~90 queries |
| Intentional Error Rate | ~8–10% of records |

The entire workflow — from raw data to final report — is implemented using only **pandas, numpy, and matplotlib**, kept deliberately beginner-friendly (no advanced OOP, no complex list comprehensions, no decorators) so that the code is easy to read, explain in an interview, and extend.

---

## 2. Clinical Data Management Overview

**Clinical Data Management (CDM)** is the discipline within clinical research responsible for producing high-quality, reliable, and statistically sound data from clinical trials. It sits at the intersection of clinical operations, biostatistics, and regulatory compliance.

A typical CDM lifecycle includes:

1. **Study Start-Up** — Designing the eCRF, writing the Data Management Plan (DMP), and defining validation/edit-check rules based on the protocol.
2. **Data Collection** — Sites enter subject data into the Electronic Data Capture (EDC) system as visits occur.
3. **Data Validation** — Automated and manual checks are run against the incoming data to catch missing values, out-of-range results, logical inconsistencies, and protocol deviations.
4. **Query Management** — When an issue is found, a data query is raised, sent to the site, and tracked until it is answered and resolved.
5. **Medical Coding** — Adverse events and concomitant medications are coded using standard dictionaries (e.g., MedDRA, WHO-DD).
6. **Database Lock** — Once all queries are resolved and data is verified as clean, the database is locked and released for statistical analysis.
7. **Reporting & Archival** — Final datasets and audit trails are archived per regulatory requirements (e.g., 21 CFR Part 11, ICH-GCP).

A Clinical Data Coordinator typically supports steps 3 and 4 — this project is built specifically around that part of the workflow.

---

## 3. What is an eCRF?

An **electronic Case Report Form (eCRF)** is the digital form used to capture all protocol-required data for each subject at each study visit. It replaces the older paper CRF and is typically hosted inside an EDC system such as Medidata Rave, Oracle Clinical, or Veeva Vault.

Each eCRF is broken into **forms** aligned to sections of the study protocol, for example:

- Demographics
- Vital Signs
- Adverse Events
- Concomitant Medications
- Lab Results
- ECG
- Informed Consent

In this project, our synthetic raw dataset (`raw_ecrf_data.csv`) represents a **flattened extract** of several of these forms combined into a single subject-visit level table — a common way data is exported from an EDC system for downstream review and analysis.

---

## 4. Why Data Validation Matters

Clinical trial data ultimately supports decisions about whether a drug or device is **safe and effective**. Poor data quality can:

- Delay regulatory submissions (FDA, EMA, etc.)
- Undermine the statistical validity of trial results
- Mask real safety signals (e.g., a genuinely abnormal heart rate hidden among data entry errors)
- Lead to costly re-monitoring, re-training, or re-collection of data
- In serious cases, result in regulatory findings or rejected submissions

Because of this, **every field on every eCRF is checked** against a set of validation rules before it is considered "clean." These checks generally fall into a few categories, all of which are represented in this project:

- **Mandatory field checks** — Is a required field missing? (e.g., missing Subject ID)
- **Range checks** — Is a numeric value outside a clinically plausible range? (e.g., Heart Rate > 180 bpm)
- **Valid value checks** — Does a coded field contain an allowed value? (e.g., Sex = "Male"/"Female" only)
- **Logic checks** — Are two related fields inconsistent? (e.g., Visit Date before Consent Date)
- **Duplicate checks** — Has the same subject or visit been entered more than once?

This project implements all five categories.

---

## 5. Project Workflow

```
 ┌─────────────────────┐
 │  Raw eCRF Export     │   raw_ecrf_data.csv
 │  (with data errors)  │
 └──────────┬───────────┘
            │
            ▼
 ┌─────────────────────┐
 │  Validation Script    │   scripts/validate_ecrf.py
 │  (edit-check rules)   │
 └──────────┬───────────┘
            │
   ┌────────┴────────┐
   ▼                 ▼
┌───────────────┐ ┌─────────────────────────┐
│ Cleaned Data  │ │ Discrepancy Query Log    │
│ .csv          │ │ .csv                     │
└───────┬───────┘ └────────────┬────────────┘
        │                      │
        └──────────┬───────────┘
                    ▼
        ┌───────────────────────┐
        │ Jupyter Notebook       │
        │ (exploration + charts) │
        └───────────┬───────────┘
                    ▼
        ┌───────────────────────┐
        │ Validation Summary /   │
        │ PDF Data Quality Report│
        └───────────┬───────────┘
                    ▼
        ┌───────────────────────┐
        │ Dashboard Mockup       │
        └───────────────────────┘
```

**Step-by-step:**

1. Synthetic raw eCRF data is generated, deliberately including realistic CDM errors.
2. `validate_ecrf.py` scans the raw data row by row using simple `for` loops and `if` statements, flags issues, and produces a cleaned dataset plus a discrepancy query log.
3. The Jupyter notebook loads all three data files and performs exploratory analysis, missing value/duplicate checks, query log analysis, and visualization.
4. Key metrics are consolidated into `validation_summary.csv` and a formatted PDF report.
5. A dashboard mockup visualizes the same KPIs in a stakeholder-friendly format.

---

## 6. Folder Structure

```
Clinical-eCRF-Validation/
│
├── data/
│   ├── raw_ecrf_data.csv              # Raw, unvalidated eCRF export (~900 rows)
│   ├── cleaned_ecrf_data.csv          # Post-validation cleaned dataset
│   ├── discrepancy_query_log.csv      # Data query tracking log (~90 queries)
│   └── protocol_validation_rules.xlsx # Edit-check rule reference table
│
├── notebooks/
│   └── 01_eCRF_Data_Validation_Analysis.ipynb   # Full exploratory + validation analysis
│
├── scripts/
│   └── validate_ecrf.py               # Beginner-friendly validation script
│
├── reports/
│   ├── validation_summary.csv         # Final KPI summary table
│   └── data_quality_report.pdf        # Formatted data quality report
│
├── dashboard/
│   └── dashboard_mockup.png           # Visual KPI dashboard mockup
│
├── README.md                          # This file
│
└── requirements.txt                   # Python dependencies
```

---

## 7. Validation Rules

Validation rules used in this project are documented in `data/protocol_validation_rules.xlsx` and mirrored in the validation script. A summary of the rule categories:

| Rule Type | Example Field | Rule |
|---|---|---|
| Mandatory Field | Subject_ID | Must not be blank |
| Mandatory Field | Visit_Date | Must not be blank |
| Mandatory Field | Informed_Consent_Date | Must not be blank |
| Range Check | Heart_Rate_bpm | Must be between 40–180 bpm |
| Range Check | Systolic_BP_mmHg | Must not exceed 200 mmHg |
| Range Check | Temperature_C | Must be between 34.0–42.0 °C |
| Valid Value Check | Sex | Must be "Male" or "Female" |
| Logic Check | Visit_Date vs Informed_Consent_Date | Visit cannot occur before consent |
| Logic Check | Visit_Date | Cannot be a future date |
| Duplicate Check | Subject_ID | Should not repeat unexpectedly across records |

Each rule is assigned a **severity** (Critical, Major, Minor) reflecting its impact on subject safety, data integrity, or regulatory compliance — the same triage logic used in real EDC systems like Medidata Rave or Oracle InForm.

---

## 8. Dataset Description

### 8.1 `raw_ecrf_data.csv`

The raw dataset simulates a flattened eCRF export across 300 subjects, 5 sites, and 3 visits (Screening, Baseline, Week 4), totaling approximately 900 rows (906 including intentional duplicate records).

| Column | Description |
|---|---|
| Site_ID | Investigational site identifier (SITE001–SITE005) |
| Subject_ID | Unique subject identifier |
| Visit | Scheduled visit name |
| Visit_Date | Date the visit occurred |
| Informed_Consent_Date | Date the subject signed informed consent |
| Age | Subject age in years |
| Sex | Subject sex |
| Height_cm | Height in centimeters |
| Weight_kg | Weight in kilograms |
| BMI | Body Mass Index |
| Heart_Rate_bpm | Heart rate in beats per minute |
| Respiratory_Rate | Breaths per minute |
| Temperature_C | Body temperature in Celsius |
| Systolic_BP_mmHg | Systolic blood pressure |
| Diastolic_BP_mmHg | Diastolic blood pressure |
| Lab_Status | Normal / Abnormal / Not Done |
| ECG_Status | Normal / Abnormal / Not Done |
| Adverse_Event | Reported adverse event, if any |
| Concomitant_Medication | Reported concomitant medication, if any |
| Investigator_Name | Principal investigator at the site |
| Data_Entry_Date | Date the record was entered into the EDC |

### 8.2 Intentional Data Quality Issues

To make the dataset realistic, approximately 8–10% of records contain deliberately introduced errors, including:

- Missing Subject ID, Age, Weight, Visit Date, or Consent Date
- Missing Investigator Name
- Heart Rate above 180 bpm or below 40 bpm
- Systolic Blood Pressure above 200 mmHg
- Temperature above 42°C or below 34°C
- Invalid Sex values (e.g., "M", "Unknown", "X")
- Visit Date recorded before Consent Date
- Future-dated visits
- Duplicate Subject IDs and duplicate visit rows

### 8.3 `cleaned_ecrf_data.csv`

The cleaned dataset reflects the dataset after the validation script has run: rows with unrecoverable critical errors (e.g., missing Subject ID, missing Visit Date) are removed, while minor gaps (e.g., missing Age or Weight) are imputed using simple statistical measures (median), consistent with common interim cleaning practices before full query resolution.

### 8.4 `discrepancy_query_log.csv`

Each row represents a single data query raised against a specific subject, visit, and field, including:

- Query_ID, Site_ID, Subject_ID, Visit
- Form_Name, Field_Name
- Error_Type, Error_Description
- Query_Status (Open, Answered, Closed, Cancelled)
- Priority (High, Medium, Low)
- Action_Required
- Query_Date, Resolution_Date

---

## 9. Notebook Walkthrough

`notebooks/01_eCRF_Data_Validation_Analysis.ipynb` is structured as a guided, markdown-annotated analysis with the following sections:

1. **Introduction** — project context and objectives
2. **Load Dataset** — import libraries, load raw/cleaned/query data
3. **Dataset Overview** — shape, columns, head, info, describe
4. **Missing Value Analysis** — counts and percentages per column
5. **Duplicate Analysis** — full-row duplicates and duplicate Subject IDs
6. **Query Log Analysis** — status, error type, and priority breakdowns
7. **Subject Level Analysis** — queries per subject
8. **Site Level Analysis** — queries and records per site
9. **Vital Signs Analysis** — descriptive stats and out-of-range flags
10. **Visit Analysis** — visit distribution and visit-before-consent checks
11. **Data Completeness** — overall and per-site completeness scoring
12. **Error Frequency** — most common error and field types
13. **Charts** — histograms, bar charts, a pie chart, a boxplot, and a correlation heatmap, all built with matplotlib
14. **Final Data Quality Report** — a consolidated KPI table, saved to `reports/validation_summary.csv`
15. **Recommendations** — clinical interpretation, data quality recommendations, and future work

The notebook is designed to run **top to bottom without modification**, provided the `data/` folder is populated as described above.

---

## 10. Output Files

| File | Description |
|---|---|
| `reports/validation_summary.csv` | Final KPI table: total records, total/open/closed queries, error rate, missing values, protocol deviations, and overall completeness |
| `reports/data_quality_report.pdf` | Formatted, stakeholder-ready PDF summarizing KPIs, error breakdowns, charts, and recommendations |
| `dashboard/dashboard_mockup.png` | Visual dashboard mockup showing headline metrics and supporting charts |

---

## 11. Dashboard

The dashboard mockup (`dashboard/dashboard_mockup.png`) illustrates how the same metrics computed in the notebook could be surfaced to a study team in a lightweight BI tool (e.g., Power BI, Tableau, or a simple internal web dashboard). It includes:

**Summary Cards**
- Total Records
- Open Queries
- Closed Queries
- Error Rate

**Charts**
- Queries by Site
- Queries by Field
- Query Status Breakdown
- Most Common Error Types

This mockup demonstrates the ability to translate raw analysis into a format non-technical stakeholders (Clinical Operations, Biostatistics, Sponsor teams) can act on quickly.

---

## 12. Clinical Relevance

Every check performed in this project mirrors a real CDM activity:

- **Missing Subject ID / Visit Date / Consent Date** → Directly affects subject traceability and GCP compliance; these are always Critical-priority queries in real trials.
- **Out-of-range vital signs** → Could indicate a genuine safety signal (requiring investigator/medical monitor review) or a transcription error — this project shows why data managers never "just delete" such values without querying the site.
- **Visit before Consent** → A serious protocol deviation, since no study procedure may occur before a subject has consented; this is exactly the kind of logic check embedded in real EDC edit-check specifications.
- **Duplicate Subject IDs / visits** → Common in multi-site trials with manual or semi-manual data entry; left unresolved, duplicates inflate subject counts and bias statistical analysis.
- **Query aging (Open vs Closed)** → Real trials track "query turnaround time" as a core CDM KPI, since unresolved queries delay database lock and, ultimately, submission timelines.

---

## 13. Resume Highlights

Suggested bullet points for a resume or LinkedIn profile based on this project:

- Built an end-to-end synthetic clinical trial data validation pipeline covering 300 subjects across 5 sites, identifying and logging ~90 data discrepancies against protocol-defined edit-check rules.
- Developed a Python-based (pandas/numpy) validation script to detect missing data, out-of-range vital signs, and logical inconsistencies (e.g., visit-before-consent) in eCRF data.
- Performed exploratory data analysis and data quality reporting using pandas and matplotlib, including missing value analysis, duplicate detection, and completeness scoring by site.
- Authored a Data Quality Report and KPI dashboard mockup summarizing error rates, query status, and protocol deviations for stakeholder review.
- Applied Clinical Data Management (CDM) concepts including query management, edit-check design, and data completeness metrics in a reproducible, well-documented Jupyter Notebook.

---

## 14. Interview Questions & Answers

**Q1: What is the difference between a query and a protocol deviation?**
A query is a formal request for clarification sent to a site about a specific data point (e.g., "Please confirm subject's weight at Visit 2"). A protocol deviation is an instance where the study was not conducted according to the approved protocol (e.g., a visit occurring outside its allowed window, or a procedure performed before consent). A query may or may not reveal a protocol deviation once resolved.

**Q2: How would you prioritize which queries to resolve first?**
Typically by severity/priority: Critical/High-priority queries (e.g., missing consent dates, visit-before-consent) that affect subject safety, traceability, or regulatory compliance are resolved first, followed by Major queries affecting data accuracy, and finally Minor/Low-priority queries.

**Q3: What would you do if you found a Heart Rate of 220 bpm in the data?**
I would not simply delete or "correct" it. I would raise a data query to the site asking them to confirm the value against the source document, since it could be either a transcription error or a genuine clinical finding requiring investigator and/or medical monitor review.

**Q4: Why is "Visit Date before Consent Date" considered a Critical finding?**
Because it implies a study procedure may have been performed on a subject before they legally consented to participate — a serious Good Clinical Practice (GCP) and regulatory compliance issue, not just a data entry mistake.

**Q5: What tools have you used for data validation, and why did you choose pandas for this project?**
Pandas provides simple, readable tools (`isnull()`, `duplicated()`, `value_counts()`, boolean filtering) that map directly onto common CDM edit checks, making it well suited to demonstrating validation logic clearly — the same logical checks are used in EDC systems like Medidata Rave, just implemented via configured edit-check specifications rather than Python code.

**Q6: How do you ensure data completeness before database lock?**
By tracking a completeness percentage per required field and per site, resolving all outstanding critical/major queries, and re-running validation checks after each round of site corrections until no unresolved discrepancies remain.

---

## 15. Future Improvements

- Automate the validation script to run on a schedule against new eCRF extracts, emailing a summary to the study team.
- Add a query aging report (days open) to flag stale queries approaching an SLA breach.
- Extend the query log with a full audit trail of query text exchanged between sites and Data Management.
- Add cross-form consistency checks (e.g., comparing lab collection dates against visit dates) once additional eCRF forms are modeled.
- Rebuild the dashboard mockup as a live, interactive dashboard (e.g., Power BI, Streamlit) connected directly to the validation outputs.
- Incorporate simple statistical outlier detection (e.g., z-scores) alongside the fixed clinical range checks already implemented.

---

## Requirements

See `requirements.txt`. This project uses only:

```
pandas
numpy
matplotlib
openpyxl
```

## License

This project is provided for educational and portfolio purposes. All data is synthetic.
