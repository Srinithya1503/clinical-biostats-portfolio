# Trial Master File (TMF) Audit & Quality Metrics Engine

[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Regulatory Framework: ICH E6(R2)](https://img.shields.io/badge/Regulatory-ICH%20E6(R2)%20GCP-orange)](https://www.ich.org/page/efficacy-guidelines)
[![TMF Standard: DIA Reference Model v3.0](https://img.shields.io/badge/TMF%20Standard-DIA%20Reference%20Model%20v3.0-purple)](https://tmfrefmodel.com/)
[![Status: Portfolio Ready](https://img.shields.io/badge/Status-Portfolio%20Ready-brightgreen)]()

---

## 📋 Project Overview

This repository contains a **production-ready, end-to-end automated audit pipeline** for Trial Master File (TMF) quality monitoring in regulated clinical research environments. It was built to demonstrate fluency in the intersection of **clinical operations domain expertise**, **quantitative data analysis**, and **regulatory compliance systems thinking** — the core competencies of a Clinical Operations & Systems Analyst at a global CRO or pharmaceutical sponsor.

The engine ingests a synthetic TMF document manifest (modelled on the DIA TMF Reference Model v3.0), computes a suite of regulatory quality metrics, automatically identifies **High-Risk Non-Compliance Clusters**, and generates professional diagnostic figures suitable for inclusion in sponsor oversight reports, QA/QC packages, or regulatory inspection readiness binders.

### What Problem Does This Solve?

In a clinical trial that spans 50+ sites across 15 countries over 5 years, a TMF can contain **50,000 to 500,000 individual documents**. Manual review is:

- ❌ Impossible to scale across a full portfolio
- ❌ Inconsistent across different CRAs and document reviewers
- ❌ Too slow to support the 5–10 business day preparation window before an FDA or EMA inspection
- ❌ Unable to identify systemic patterns across sites and document zones

This engine solves all four problems by automating the detection layer, freeing Clinical Operations Analysts to focus on **remediation, stakeholder communication, and CAPA management** — the high-value work that cannot be automated.

---

### How This Engine Prevents These Outcomes

The audit engine implements **three layers of regulatory defence**:

1. **Early Warning System:** The 85% Quality Pass Rate threshold (derived from ICH E6 R2 and industry-standard sponsor TMF plans) identifies at-risk sites *months* before an inspection.

2. **Systemic Pattern Detection:** The cluster analysis distinguishes between a site with one missing document (isolated) and a site where 60% of documents lack valid signatures (systemic) — the latter requires a CAPA, not just a query.

3. **Inspection-Ready Reporting:** The output text report and diagnostic figures are formatted to be inserted directly into a Regulatory Inspection Readiness Package without reformatting.

---

## 🏗️ Repository Architecture

```
tmf_audit_engine/
│
├── 📁 data/
│   ├── synthetic_tmf_manifest.csv        # 160-row synthetic TMF dataset
│   └── generate_synthetic_data.py        # Reproducible data generation script
│
├── 📁 src/
│   └── tmf_audit_engine.py               # Core audit pipeline (fully self-contained)
│
├── 📁 docs/
│   └── TMF_LEARNING_MANUAL.md            # Comprehensive industry training manual
│
├── 📁 outputs/                           # Auto-created on first run
│   ├── figure1_noncompliance_reasons.png # Diagnostic Figure 1
│   ├── figure2_site_risk_heatmap.png     # Diagnostic Figure 2
│   └── tmf_audit_report.txt             # Full plain-text audit report
│
└── README.md                             # This file
```

---

## ✨ Core Engine Features

### 1. Clinical Quality Metric Computation

The engine calculates three primary metrics used in real-world TMF governance:

| Metric | Formula | Regulatory Relevance |
|--------|---------|---------------------|
| **Completeness Rate (%)** | Approved + No NC Reason ÷ Total × 100 | ICH E6(R2) Section 8 – Essential Documents |
| **Timeliness Gap (Days)** | Upload Date − Expected Date | SOP-defined filing windows; FDA contemporaneousness |
| **Quality Pass Rate (%)** | Approved + No Sig Issue + No NC ÷ Total × 100 | Primary KPI in sponsor TMF quality plans |

All three map directly to **ALCOA++ data integrity principles** — the internationally recognised framework for clinical data quality (Attributable, Legible, Contemporaneous, Original, Accurate + Complete, Consistent, Enduring, Available).

### 2. Composite Risk Scoring

Each site receives a **Risk Score (0–100)** derived from a weighted composite of all quality dimensions:

```
Risk Score = (100 − Quality Pass Rate) × 0.40   ← core quality gate
           + Rejection Rate            × 0.25   ← outright failures
           + Missing Signature Rate    × 0.25   ← ALCOA Attributability failures
           + min(Avg. Timeliness Gap, 60) × 0.10  ← timeliness (capped)
```

This mirrors the risk-scoring models used in **Risk-Based Quality Management (RBQM)** frameworks mandated by ICH E6(R2) and TransCelerate's RBQM principles.

### 3. High-Risk Non-Compliance Cluster Detection

Two categories of systemic failures are automatically flagged:

- **Site Clusters:** Sites where Quality Pass Rate falls below the 85% threshold
- **Zone Clusters:** DIA TMF Zones where the rejection rate exceeds 30%

Embedded systemic flaws in the synthetic dataset (designed to reflect realistic failure modes):
- **Site 102:** 60% missing signature rate → ALCOA Attributability breakdown
- **Zone 3 (Investigator Site File):** 50% rejection rate → Highest-risk TMF zone
- **Ukraine sites:** Elevated expired document rate → Country-level operational disruption
- **Sites 105 & 107:** Chronic 30–120 day late uploads → Contemporaneousness failures

### 4. Diagnostic Visualisations

| Figure | Type | Clinical Use |
|--------|------|-------------|
| **Figure 1** | Horizontal bar chart (colour-graded) | Root cause analysis of non-compliance types; prioritises which issue category to address first |
| **Figure 2** | Multi-metric site risk heatmap | Cross-site comparison; used in TMF oversight committee presentations and sponsor dashboard reporting |

Both figures are formatted to **regulatory document standards**: clear labelling, data source footnotes, date stamps, and figure numbering aligned with clinical study report conventions.

---

## 🔁 Transferable Skills Matrix

This project was engineered to demonstrate the **direct equivalence** between high-level academic and biomedical science skills and the quantitative demands of enterprise clinical operations and systems analysis.

---

## 📂 Dataset Schema Reference

The synthetic TMF manifest (`data/synthetic_tmf_manifest.csv`) contains 160 rows and the following 12 columns:

| Column | Type | Description |
|--------|------|-------------|
| `Document_ID` | String | Unique document identifier (DOC-XXXX) |
| `Study_ID` | String | Clinical study identifier |
| `Country` | String | Country where the site is located |
| `Site_ID` | Integer | Site identifier (101–108) |
| `DIA_Zone` | String | DIA TMF Reference Model Zone (1–5) |
| `DIA_Section` | String | Zone sub-section (e.g., "3.1 Site Staff & Delegation") |
| `Document_Name` | String | Specific document/artifact name |
| `Upload_Date` | Date (YYYY-MM-DD) | Actual date document was uploaded to the eTMF |
| `Expected_Date` | Date (YYYY-MM-DD) | Date by which the document was required |
| `Review_Status` | Categorical | Approved / Pending / Rejected |
| `Missing_Signature` | Boolean | True if the document lacks a required signature |
| `Non_Compliance_Reason` | Categorical | None / Expired Document / Missing Wet/Digital Signature / Incomplete Log / Artifact Mismatch / Late Submission |

---

## 📖 Learning Resources

- **`docs/TMF_LEARNING_MANUAL.md`** — Complete training manual covering: DIA TMF Reference Model architecture (all 5 Zones), ALCOA++ data integrity principles (all 8), step-by-step SOPs for resolving common TMF discrepancies, metric definitions, and a regulatory inspection readiness guide
- **[DIA TMF Reference Model](https://tmfrefmodel.com/)** — The authoritative public resource for the TMF taxonomy
- **[ICH E6(R2) GCP Guideline](https://www.ich.org/page/efficacy-guidelines)** — The primary international GCP guideline
- **[FDA Guidance on Electronic Records (21 CFR Part 11)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/part-11-electronic-records-electronic-signatures-scope-and-application)** — Governs electronic TMF systems

---

## 📄 Regulatory References

This engine was designed with reference to the following regulatory and industry frameworks:

- **ICH E6(R2)** – Good Clinical Practice: Integrated Addendum (2016)
- **FDA 21 CFR Part 312** – Investigational New Drug Application
- **FDA 21 CFR Part 11** – Electronic Records and Electronic Signatures
- **EMA GCP Inspections Working Group** – Reflection Paper on Risk-Based Quality Management
- **DIA TMF Reference Model v3.0** – Drug Information Association (2020)
- **TransCelerate BioPharma** – RBQM Implementation Guidance
- **MHRA GXP Data Integrity Guidance** (2018)
- **WHO Technical Report Series 996** – Good Clinical Practice Guidance

---

*Built to demonstrate the intersection of rigorous biomedical science training and enterprise clinical data systems — the foundation of an effective Clinical Operations & Systems Analyst.*

