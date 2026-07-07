## 📋 DATASET DETAILS (Column-by-column)

---

### `raw_dm.csv` — Demographics
| Column | Type | Description |
|---|---|---|
| STUDYID | String | Study identifier — always "ONCO-2026" |
| SITEID | String | Clinical site code (SITE001–SITE015) |
| SUBJID | String | Unique subject identifier (SUBJ0001–SUBJ0500) |
| AGE | Integer | Age at randomization in years (range: 18–85) |
| SEX | String | Biological sex — M or F |
| RACE | String | Subject race per ICH E6 categories |
| ETHNICITY | String | Hispanic/Latino status |
| HEIGHT_CM | Float | Height in centimeters (3% missing) |
| WEIGHT_KG | Float | Weight in kilograms (3% missing) |
| BMI | Float | Body Mass Index kg/m² — null if height or weight missing |
| BIRTH_DATE | Date | Date of birth (YYYY-MM-DD) |
| COUNTRY | String | ISO 3-letter country code |
| RAND_DATE | Date | Date of randomization |
| ARM | String | Treatment arm — ARM A (Drug X) or ARM B (Placebo) |
| TREATMENT_START_DATE | Date | First dose date (0–7 days after randomization) |

---

### `raw_lab.csv` — Laboratory Results
| Column | Type | Description |
|---|---|---|
| SUBJID | String | Links to raw_dm.csv |
| VISIT | String | Scheduled visit label (BASELINE / WEEK 4 / WEEK 8 / WEEK 12 / WEEK 24) |
| VISIT_DATE | Date | Actual date of lab collection |
| TEST_CODE | String | Short lab code — ALT, AST, HGB, PLT, CREAT, TUMKR |
| TEST_NAME | String | Full test name (e.g., Alanine Aminotransferase) |
| RESULT | Float | Numeric lab result |
| UNIT | String | Unit of measure (U/L, g/dL, 10^9/L, mg/dL, ng/mL) |
| REFERENCE_LOW | Float | Lower limit of normal range |
| REFERENCE_HIGH | Float | Upper limit of normal range |
| ABNORMAL_FLAG | String | H = High, L = Low, blank = Normal |

> ⚠️ Contains ~0.5% duplicate rows and ~1% outlier values by design. ~5% of individual lab results are missing. ~8% of visits are entirely skipped.

---

### `raw_ae.csv` — Adverse Events
| Column | Type | Description |
|---|---|---|
| SUBJID | String | Links to raw_dm.csv |
| AE_TERM | String | Verbatim adverse event term |
| AE_START_DATE | Date | Date the AE began |
| AE_END_DATE | Date | Date the AE ended — blank if ongoing (~10% missing) |
| SEVERITY | String | Mild / Moderate / Severe |
| SERIOUS_FLAG | String | Y = Serious Adverse Event (SAE), N = Non-serious |
| RELATED_TO_TREATMENT | String | Y = Related, N = Not related (causality assessment) |
| OUTCOME | String | Recovered / Recovering / Not Recovered / Fatal / Unknown |

> ARM A subjects average ~7 AEs each. ARM B subjects average ~4. Fatal outcomes present in ~4% of events.

---

### `raw_cm.csv` — Concomitant Medications
| Column | Type | Description |
|---|---|---|
| SUBJID | String | Links to raw_dm.csv |
| MEDICATION_NAME | String | Generic drug name |
| START_DATE | Date | Medication start date |
| END_DATE | Date | Medication end date — blank if ongoing (~8% missing) |
| DOSE | String | Dose with unit (e.g., 8 mg, 300 mcg) |
| ROUTE | String | Route of administration — ORAL, INTRAVENOUS, SUBCUTANEOUS |
| INDICATION | String | Reason for medication use |

> Medications include: Ondansetron, Dexamethasone, Morphine, Prednisone, Filgrastim, Erythropoietin, Omeprazole, Lorazepam, Ibuprofen, Metoclopramide.

---

### `raw_tumor.csv` — Tumor Response
| Column | Type | Description |
|---|---|---|
| SUBJID | String | Links to raw_dm.csv |
| ASSESSMENT_DATE | Date | Date of tumor imaging/assessment |
| TARGET_LESION_SIZE | Float | Sum of target lesion diameters in mm |
| BASELINE_LESION_SIZE | Float | Baseline reference lesion size in mm |
| PCT_CHANGE_FROM_BASELINE | Float | % change from baseline (null at baseline visit) |
| RESPONSE_CATEGORY | String | RECIST 1.1 response — CR / PR / SD / PD |

> Assessments at 4 timepoints: Day 0, ~Week 8, ~Week 16, ~Week 24. ARM A shows greater tumor shrinkage. ~4% of assessments randomly missing.

---

### `raw_survival.csv` — Overall Survival
| Column | Type | Description |
|---|---|---|
| SUBJID | String | Links to raw_dm.csv |
| DEATH_DATE | Date | Date of death — blank if subject is censored |
| LAST_FOLLOWUP_DATE | Date | Last known alive date (used as censoring date) |
| EVENT_STATUS | Integer | 1 = Death occurred, 0 = Censored |
| OS_DAYS | Integer | Overall survival days from treatment start |
| ARM | String | Treatment arm (ARM A / ARM B) — included for direct KM analysis |

> ARM A median OS ≈ 480 days. ARM B median OS ≈ 360 days. ~55% of subjects have an event (death).

---

### `raw_vitals.csv` — Vital Signs
| Column | Type | Description |
|---|---|---|
| SUBJID | String | Links to raw_dm.csv |
| VISIT | String | SCREENING / BASELINE / WEEK 4 / WEEK 8 / WEEK 12 / WEEK 24 / EOT |
| VISIT_DATE | Date | Date of vital signs collection |
| SBP | Float | Systolic blood pressure (mmHg) |
| DBP | Float | Diastolic blood pressure (mmHg) |
| HEART_RATE | Float | Heart rate (beats per minute) |
| TEMPERATURE | Float | Body temperature (°C) |

> ~7% of visits skipped per subject. Subject-level baseline variation simulated (each patient has their own physiological baseline).

---

### `raw_pd.csv` — Protocol Deviations
| Column | Type | Description |
|---|---|---|
| SUBJID | String | Links to raw_dm.csv |
| DEVIATION_CATEGORY | String | Type of deviation (see categories below) |
| DESCRIPTION | String | Standardized description of the deviation |
| DATE | Date | Date the deviation occurred |

---
> Deviation categories: Missed Visit, Late Lab Collection, Wrong Dose Administered, Inclusion/Exclusion Criteria Violation, Prohibited Medication, Consent Deviation, Late AE Reporting, Equipment Calibration. ~40% of subjects have zero deviations.

---


— column-level detail for each file, and a full description that will rank well in search and immediately signal value to your target audience (SAS programmers, biostatisticians, CDISC mappers). The disclaimer at the bottom is important to include for synthetic medical datasets.
