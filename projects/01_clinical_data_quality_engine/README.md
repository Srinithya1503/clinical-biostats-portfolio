# Clinical Trial Data Validation Engine

> Automated Edit Check Suite for Clinical Trial Data Integrity
> CDISC SDTM · ICH E6(R2) GCP · ICH E2A · CTCAE v5.0.


This suite contains tool validate clinical trial data against common clinical data management rules. It helps identify data entry errors, protocol deviations, and logical inconsistencies before data analysis.

---

## Data Schema

The project dataset populates three core relational tables:

### 1. `patients.csv` (200 rows)
* Contains baseline patient demographics.
* **Key fields**: Patient ID, Age, Gender, Consent Date, Pregnancy Status.

### 2. `visits.csv` (1,400 rows)
* Tracks longitudinal data over 7 standard visits per patient.
* **Key fields**: Patient ID, Visit ID, Visit Date, Systolic BP, Diastolic BP.

### 3. `adverse_events.csv` (409 rows)
* Logs safety events reported during the trial.
* **Key fields**: Patient ID, AE ID, Start Date, End Date, Severity, Serious (Y/N), Fatal (Y/N).

---

## Repository Structure

```
clinical-data-validation-engine/
├── edit_check_engine.py      
├── requirements.txt          
├── dataset_manual.md 
├── issues_found.csv
├── .gitignore
├── README.md         
└── data/                     
    ├── patients.csv
    ├── subject_visits.csv
    └── adverse_events.csv
```
---

## Validation Rules Reference

The validation engine executes 7 primary logical checks. Discrepancies are flagged by severity (**Critical**, **Major**, **Minor**) and compiled into `issues_found.csv`.

| Check ID | Name | Description | Severity |
| :--- | :--- | :--- | :--- |
| **CHK-01** | Age Range Check | Flags patients outside the protocol-defined age limits. | Major |
| **CHK-02** | Gender/Pregnancy | Flags logical errors (e.g., pregnancy positive in male patients). | Critical |
| **CHK-03** | Blood Pressure (Systolic) | Flags systolic blood pressure values out of clinical bounds. | Critical |
| **CHK-03B** | Blood Pressure (Diastolic) | Flags diastolic blood pressure values out of clinical bounds. | Critical |
| **CHK-04** | Visit Before Consent | Flags clinical visits dated prior to the patient's informed consent date. | Critical |
| **CHK-05A** | AE Start Date | Flags adverse events starting before the informed consent date. | Critical |
| **CHK-05B** | AE Timeline | Flags adverse events where the resolution date precedes the start date. | Critical |
| **CHK-06** | Fatal = Serious | Flags logical errors where an event is marked "Fatal" but not "Serious". | Critical |
| **CHK-07** | Serious Severity | Ensures all serious adverse events have an assigned severity level. | Minor |

---

## Execution Guide

### Prerequisites
Ensure you have Python 3.x installed along with the `pandas` library.
```bash
pip install pandas
```
### Step 1: Run Validation Checks
Run the validation engine to scan the files and output the error log.
```bash
python edit_check_engine.py
```

---

## Output Logs

Upon completion, the engine generates **`issues_found.csv`**. This file catalogs all 223 discovered issues and contains the following columns for easy filtering:
* `Patient_ID`
* `Check_ID`
* `Severity`
* `Description_of_Error`
* `Value_Found`

---

## Data Quality Insights & Conclusions

An analysis of the validation output reveals critical operational insights based on the concentration of data discrepancies:

1. **Systemic Site-Level Issues:** The high concentration of errors in specific patient files (e.g., `PT-106` and `PT-019` with 5 issues each) strongly indicates systematic data entry errors or process failures. This typically points to a specific clinical site or coordinator requiring immediate retraining.
2. **Protocol Non-Compliance:** Accumulating 4 to 5 distinct issues over just 7 visits suggests potential protocol deviations, such as missing protocol windows, enrolling ineligible subjects, or failing to follow safety reporting workflows.
3. **Patient Safety Risks:** Because the majority of the engine's flags are categorized as **Critical** (e.g., adverse event timeline contradictions or severe blood pressure anomalies), these specific high-error patients may represent actual clinical instability that is being poorly recorded.
4. **Regulatory Audit Exposure:** Regulatory bodies (such as the FDA or EMA) routinely screen for high-error outliers during inspections. These 5 patient profiles represent immediate audit risks; their source documentation must be manually cross-referenced against the database.

---

## Standards & Regulatory Alignment

| Standard | Application in this Project |
|---------|----------------------------|
| **ICH E6(R2) GCP** | EC-SV-05: No procedures before informed consent |
| **ICH E2A** | EC-AE-03: Fatal AE must be classified as Serious |
| **CTCAE v5.0** | EC-AE-05: Severity grading required for all SAEs |
| **CDISC SDTM IG v3.3** | Domain naming, required variables (EC-DM-04) |
| **21 CFR Part 11** | Audit trail design principles in architecture |

---

*Built to demonstrate CDM programming competency for a Clinical Data Management Programmer I role. All patient data is entirely synthetic — no real subject data is used or referenced.*
