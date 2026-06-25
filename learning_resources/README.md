# Clinical Data Domain & Biostatistics Technical Reference Library

## Overview

This repository serves as a structured learning and reference library covering the complete clinical research data lifecycle.It establishes the theoretical foundation supporting the technical projects developed in this portfolio, including:

- Clinical Data Management workflows
- TMF compliance analytics
- Clinical trial documentation
- CDISC standards
- Statistical programming
- Biostatistical analysis
- Regulatory reporting

---
## Clinical Research Data Lifecycle Map

Clinical Trial Design

↓

Regulatory Approval

↓

Clinical Operations

↓

Data Collection

↓

Clinical Data Management

↓

CDISC Standardization

↓

Statistical Analysis

↓

Clinical Reporting

↓

Regulatory Submission

---

## Knowledge Map

### [01. Regulatory & Quality Frameworks](01_Reg_Quality_Standards)
**Purpose:**
Understand the compliance principles governing clinical research.

**Topics:**
- ICH-GCP E6(R2/R3)
- ALCOA+ Data Integrity Principles
- FDA 21 CFR Part 11
- Regulatory Inspection Readiness
  
---

### 02. Clinical Trial Operations
**Topics:**
- Trial lifecycle
- Trial phases
- Study team roles
- Essential documents

---

### 03. Clinical Data Management
**Purpose:**
Ensure collected clinical data is accurate, complete, and ready for analysis.

**Topics:**
- CRF design
- Database setup
- Data cleaning
- Edit checks
- Query management
- Medical coding
- Database lock

**Example Workflow:**

Data Entry

↓

Validation Rules

↓

Queries

↓

Data Cleaning

↓

Lock

↓

Analysis

---

### 04. Trial Master File (TMF)
**Purpose:** 
Understand clinical document compliance and inspection readiness.

**Topics:**
- DIA TMF Reference Model
- TMF Zones
- Essential Documents
- Reconciliation
- Audit Preparation

---

### 05. CDISC Standards
**Purpose:**
Learn industry-standard clinical data structures.

**1.CDASH** - Data collection standard
**2.SDTM** - Regulatory submission tabulation model
             Examples: DM - Demographics, AE - Adverse Events, LB - Laboratory Results
**3.ADaM** - Analysis-ready datasets
             Examples:ADSL, ADTTE
             
---

### 06. Biostatistics Foundations
**Topics:**
**1.Analysis Populations**
ITT: All randomized subjects
PP: Subjects completing protocol requirements
Safety Population: Subjects receiving treatment

**2.Statistical Methods**
Descriptive statistics
Hypothesis testing
ANOVA
ANCOVA
Regression
Survival analysis

---

### 07. Clinical Statistical Programming
**Languages:**
- SAS
- R
- Python

**Topics:**
**1.SAS:** DATA step, PROC procedures, Macros
**2.Clinical Programming:**
Raw Data

↓

SDTM

↓

ADaM

↓

TLFs

---

### 08. Statistical Reporting
**Topics:**
- Statistical Analysis Plan
- Tables Listings Figures
- Clinical Study Report
- Regulatory submission outputs

---

## Recommended Learning Resources
### 1. Clinical Trials:
* Good Clinical Practice — The essential international ethical and quality standard for designing, conducting, and reporting clinical trials.
* A Guide to Perfect Clinical Trials — A comprehensive manual for managing operational workflows, documentation, and regulatory compliance.

### 2. Biostatistics:
* Fundamentals of Biostatistics by Bernard Rosner — View Resource — The foundational text covering statistical methods, hypothesis testing, and data analysis applied to clinical research.

### 3. Clinical SAS:
* SAS Programming in the Pharmaceutical Industry by Chris Holland — The golden standard manual for understanding clinical dataset mapping.
* Implementing CDISC Using SAS: An End-to-End Guide by Chris Holland and Jack Shostak — A complete guide to implementing SDTM and ADaM standards for regulatory submissions.

---

## Regulatory Websites
* **[CDISC Official Website](https://cdisc.org):** Access documentation, implementation guides, and conformance rules for SDTM, ADaM, and CDASH standards.
* **[FDA (U.S. Food and Drug Administration)](https://fda.gov):** Source for formal regulatory guidance documents on electronic data submission, validation software updates, and clinical trials rules.
* **[EMA (European Medicines Agency)](https://europa.eu):** Guidelines regarding EU clinical trial regulations, GCP oversight, and data transparency frameworks.

---

## Programming & Free Educational Platforms
* **[SAS Support & Documentation](https://sas.com):** Master repository for syntax guides, syntax error troubleshooting, and `PROC` user guides.
* **[PharmaSUG / Lex Jansen](https://lexjansen.com):** An invaluable, freely searchable index containing thousands of past whitepapers covering clinical SAS programming, macro optimization, and CDISC workflows.
* **[NIDA Blending Initiative (National Institute on Drug Abuse)](https://ctnlibrary.org):** Provides exceptional free training modules, clinical dataset examples, and standard GCP implementation training courses.
* **[Pharmaverse](https://pharmaverse.org):** An open-source collection of curated R and Python packages designed specifically for clinical reporting and CDISC-compliant dataset creation.

---

