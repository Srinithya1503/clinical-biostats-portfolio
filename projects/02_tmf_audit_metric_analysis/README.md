# Trial Master File (TMF) Audit & Quality Metrics Engine

[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Regulatory Framework: ICH E6(R2)](https://img.shields.io/badge/Regulatory-ICH%20E6(R2)%20GCP-orange)](https://www.ich.org/page/efficacy-guidelines)
[![TMF Standard: DIA Reference Model v3.0](https://img.shields.io/badge/TMF%20Standard-DIA%20Reference%20Model%20v3.0-purple)](https://tmfrefmodel.com/)
[![Status: Portfolio Ready](https://img.shields.io/badge/Status-Portfolio%20Ready-brightgreen)]()

---
**Project Identification:** TMF-RECON-ONCO-2023-001  
**Target Function:** Clinical Operations, Quality Assurance, & Project Support Coordination  

## 1. Executive Summary & Business Impact
In global clinical trials, an incomplete or non-compliant Trial Master File (TMF) poses an immediate risk of regulatory halts during FDA, EMA, or PMDA inspections. This project establishes an advanced document control framework designed to monitor, track, and reconcile essential clinical documentation for multi-national Study `ONCO-2023-001` (spanning India, Germany, USA, Japan, and the UK).

By cross-referencing raw multi-country tracking manifests against international regulatory standards (**ICH E6(R3) Section 8** and the **DIA TMF Reference Model**), this framework quantifies site-level data integrity, isolates process rejections, and builds automated query lifecycles to guarantee audit readiness.

---
## 2. Core Project Deliverables
The project framework tracks clinical document metadata across four distinct, interconnected validation tabs within the master spreadsheet asset (`TMF_Audit_Discrepancy_Log_Output.xlsx`):

* **`DIA_Reference_Map` (Master Controls):** Establishes the study baselines, assigning every expected artifact (e.g., FDA Form 1572, Investigator CVs, IMP Logs) to its corresponding regulatory basis, criticality tier, and maximum acceptable timeliness window.
* **`Reconciled_Audit_Log` (The Audit Engine):** Consolidates raw records and dynamically computes operational timeline variances (`Timeliness_Gap_Days`) while automatically identifying Good Documentation Practice (GDP) or ALCOA+ breaches.
* **`Site_Performance_Summary` (Executive Scorecard):** Aggregates document outcomes by individual investigator sites to track metrics like *Completeness Rates*, *Quality Pass Rates*, and *Missing Signature Frequencies*.
* **`High_Risk_Sites` (CAPA Escalation Tracker):** Automatically isolates and flags investigator sites falling beneath the regulatory safety threshold (<85% Quality Pass Rate) to initiate formal Corrective and Preventive Actions.
* **`Discrepancy_Query_Log` (Operational Interface):** Extracts active non-compliance observations into a high-visibility tracker to allow Project Support Coordinators to deploy mass mailings and coordinate issues with field CRAs.

---

## 3. Core Competencies Demonstrated

### Clinical Domain Mastery
* **DIA TMF Reference Model Layout:** Practical experience navigating Zone structures (Zone 1: Trial Management, Zone 3: Site Management, Zone 5: Central Lab).
* **Regulatory Frameworks:** Alignment with ICH E6(R3) Section 8 requirements for study start-up, conduct, and closeout milestones.
* **Data Integrity Verification:** Active checking for ALCOA+ core attributes (Attributable, Contemporaneous, Complete, Accurate, and Current records).

### Advanced Information Management & Excel Analytics
* Multi-sheet transactional data compilation and variable cross-referencing.
* Array calculations, timeline filtering, and logical threshold formatting.
* Transitioning unstructured operational logs into highly clean, systemized tracking matrices.

