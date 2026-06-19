# Dataset Guide
### Understanding the Three Data Tables This Project Creates

> This manual explains what data is in each CSV file, what every column means,
> and why clinical trials collect this information in real life.

---

## Overview: The Three Tables

This project creates three CSV files that together form a mini clinical trial database.

```
patients.csv            visits.csv              adverse_events.csv
─────────────           ──────────────          ────────────────────
One row                 One row per             One row per
per patient.            visit per patient.      side effect reported.

200 rows                1,400 rows              ~400 rows
                        (200 × 7 visits)        (variable per patient)
```

**How they connect:**
All three tables share the `Patient_ID` column. This is called a **primary key** — it lets you look up a patient in any table and see their full story across all three.

```
patients.csv                  visits.csv               adverse_events.csv
──────────────                ───────────────────────  ──────────────────────
Patient_ID: PT-042   ←────→  Patient_ID: PT-042  ←→  Patient_ID: PT-042
Age: 34                       Visit: Week 4             Side_Effect: Nausea
Gender: Female                Systolic_BP: 118          Severity: Mild
...                           ...                       ...
```

---

## Table 1: patients.csv

**What is it?**
The master list of everyone enrolled in the trial. One row = one person.

**Real-world name:** Demographics Domain (abbreviated as **DM** in CDISC SDTM)

### Column-by-column guide

| Column | Example Value | What it means | Why it's collected |
|--------|--------------|---------------|-------------------|
| `Patient_ID` | `PT-042` | Unique ID for this patient. Never contains their real name (privacy). | Links this patient across all three tables |
| `Site_ID` | `SITE-B` | Which clinic location they attended | Helps identify if one clinic has worse data quality |
| `Gender` | `Male` | Patient's gender | Some drugs affect men and women differently; required for safety analysis |
| `Age` | `34` | Age in years at enrollment | Determines eligibility; affects drug metabolism |
| `Treatment_Group` | `Drug 50mg` | Which drug (or placebo) they were assigned | The core of the trial — did the drug work? |
| `Consent_Date` | `2023-03-15` | The day they signed the agreement to join | **Critical** — no study activity allowed before this date |
| `Weight_kg` | `71.4` | Body weight in kilograms | Used to calculate correct drug dosage |
| `Height_cm` | `165.2` | Height in centimetres | Combined with weight to calculate BMI |
| `Pregnancy_Test_Done` | `Yes` / `No` | Whether a pregnancy test was completed | Required for female patients before starting most drugs |
| `Country` | `USA` | Country of the patient's clinic | Required for regulatory submissions in each country |

### What "valid" looks like

| Column | Valid Range / Values | Red Flag |
|--------|---------------------|----------|
| `Age` | 18 to 80 | Negative, 0, over 100 |
| `Gender` | Male, Female | Anything else |
| `Weight_kg` | 30 to 300 | Negative, 0, or over 400 |
| `Height_cm` | 100 to 250 | Negative, 0, or over 300 |
| `Pregnancy_Test_Done` | Yes or No | "Yes" when Gender is Male |
| `Country` | Any real country name | Blank / empty |

---

## Table 2: visits.csv

**What is it?**
A record of every check-up visit, with measurements taken at each one.

**Real-world names:**
- Subject Visits domain (**SV**) — tracks which visits occurred
- Vital Signs domain (**VS**) — tracks measurements like blood pressure

### The visit schedule

Each patient has 7 scheduled visits:

| Visit Name | When It Happens | Purpose |
|-----------|----------------|---------|
| Screening | 7 days before start | Check if the patient qualifies |
| Baseline | Day 0 (start) | Measure everything before the drug starts |
| Week 2 | 14 days in | Early check — is anything going wrong? |
| Week 4 | 28 days in | First month check |
| Week 8 | 56 days in | Mid-trial checkpoint |
| Week 12 | 84 days in | Three-month checkpoint |
| End of Study | 90 days in | Final measurements |

### Column-by-column guide

| Column | Example Value | What it means | Why it's collected |
|--------|--------------|---------------|-------------------|
| `Patient_ID` | `PT-042` | Which patient attended | Links back to patients.csv |
| `Visit_Name` | `Week 4` | Which scheduled visit this is | Tracks which timepoints have data |
| `Visit_Date` | `2023-04-12` | Calendar date of the visit | Must be after Consent_Date (GCP rule) |
| `Consent_Date` | `2023-03-15` | Patient's consent date (copied here for checking) | Used by CHK-04 to detect chronological errors |
| `Systolic_BP` | `118` | Top number of blood pressure (mmHg) | Monitors heart health throughout the trial |
| `Diastolic_BP` | `76` | Bottom number of blood pressure (mmHg) | Diastolic must always be lower than systolic |
| `Heart_Rate` | `72` | Heartbeats per minute | Safety monitoring |
| `Temperature_C` | `36.8` | Body temperature in Celsius | Fever can indicate infection or drug reaction |
| `Attended` | `Yes` / `No` | Did the patient show up? | Tracks missing data and compliance |

### What "valid" looks like

| Column | Valid Range | Red Flag |
|--------|------------|----------|
| `Systolic_BP` | 60 to 250 mmHg | 0, negative, over 300 |
| `Diastolic_BP` | 30 to 150 mmHg | 0, negative, or HIGHER than systolic |
| `Heart_Rate` | 30 to 250 bpm | 0, negative, over 300 |
| `Temperature_C` | 34.0 to 42.5 °C | Under 30 or over 50 |
| `Visit_Date` | Must be ≥ Consent_Date (except Screening) | Any non-screening visit before consent |

### Why blood pressure has two numbers

```
  SYSTOLIC (top)  ─────  The pressure when your heart BEATS (pumps blood out)
       120
        /
      ─── (a real reading looks like "120/80")
        \
       80
  DIASTOLIC (bottom) ──  The pressure when your heart RESTS (between beats)
```

The diastolic (bottom) number is ALWAYS lower than systolic (top). If the data shows `Diastolic = 140, Systolic = 110`, someone made a data entry mistake — those two numbers are swapped.

---

## Table 3: adverse_events.csv

**What is it?**
A record of every side effect (bad reaction) any patient experienced during the trial.

**Real-world name:** Adverse Events domain (**AE** in CDISC SDTM)

### Column-by-column guide

| Column | Example Value | What it means | Why it's collected |
|--------|--------------|---------------|-------------------|
| `AE_Number` | `17` | A unique number for each event | Identifies specific events in queries |
| `Patient_ID` | `PT-042` | Which patient had this reaction | Links back to patients.csv |
| `Side_Effect` | `Nausea` | What happened (medical term: "adverse event term") | The core data point — what went wrong |
| `Severity` | `Mild` | How bad it was | Mild / Moderate / Severe |
| `Is_Serious` | `Yes` | Does this qualify as a Serious AE? | Serious AEs have legal reporting timelines |
| `Start_Date` | `2023-04-03` | When the side effect started | Must be after Consent_Date |
| `End_Date` | `2023-04-10` | When it resolved | Must be after Start_Date |
| `Consent_Date` | `2023-03-15` | Patient's consent date (for checking) | Used by CHK-05 |
| `Outcome` | `Recovered` | What happened in the end | Fatal, Recovered, Still Recovering, etc. |

### What "valid" looks like

| Column | Valid Values | Red Flag |
|--------|-------------|----------|
| `Severity` | Mild, Moderate, Severe | Blank (especially if Is_Serious = Yes) |
| `Is_Serious` | Yes, No | "No" when Outcome is "Fatal" |
| `Start_Date` | Must be ≥ Consent_Date | Any AE starting before the patient joined |
| `End_Date` | Must be ≥ Start_Date | End date before start date |
| `Outcome` | Recovered, Still Recovering, Not Recovered, Fatal | Other values |

### What makes a side effect "Serious"?

In real clinical trials, a Serious Adverse Event (SAE) is any event that:

- Results in **death**
- Is **life-threatening**
- Requires **hospitalisation**
- Results in **permanent disability**
- Is a **birth defect**

Serious events must be reported to health authorities (like the FDA) within **7 days** of being discovered. Missing this deadline is a legal violation.

This is why **CHK-06** (Fatal must be Serious) is flagged as Critical — because if it's missed, a required safety report could be late.

---

## The Intentional Errors — A Reference Table

This project deliberately plants errors in the data to exercise the checks. Here is a complete reference of every type of error and approximately how often it appears:

| Error Type | Table | Column | Approximate Rate | Check That Catches It |
|-----------|-------|--------|-----------------|----------------------|
| Impossible age (negative or 999) | patients | Age | 3% of patients | CHK-01 |
| Male patient with pregnancy test done | patients | Pregnancy_Test_Done | 4% of male patients | CHK-02 |
| Impossible weight | patients | Weight_kg | 2% of patients | (manual review) |
| Missing country | patients | Country | 2% of patients | (manual review) |
| Impossible systolic BP | visits | Systolic_BP | 3% of visits | CHK-03 |
| Diastolic higher than systolic | visits | Diastolic_BP | 2% of visits | CHK-03B |
| Impossible heart rate | visits | Heart_Rate | 2% of visits | (can add CHK-08) |
| Impossible temperature | visits | Temperature_C | 2% of visits | (can add CHK-09) |
| Visit before consent date | visits | Visit_Date | 2% of visits | CHK-04 |
| AE end date before start date | adverse_events | End_Date | 3% of AEs | CHK-05A |
| AE started before consent date | adverse_events | Start_Date | 4% of AEs | CHK-05B |
| Fatal outcome, not marked Serious | adverse_events | Is_Serious | 2.5% of AEs | CHK-06 |
| Serious AE with blank severity | adverse_events | Severity | 3% of serious AEs | CHK-07 |

---

## What Does "Clean" Data Look Like?

Here is an example of a patient with completely clean data across all three tables:

**patients.csv row:**
```
PT-077 | SITE-C | Female | 42 | Drug 100mg | 2023-04-01 | 65.3 | 162.1 | Yes | USA
```

**visits.csv rows (first 2 visits):**
```
PT-077 | Screening | 2023-03-25 | 2023-04-01 | 118 | 76 | 70 | 36.7 | Yes
PT-077 | Baseline  | 2023-04-01 | 2023-04-01 | 122 | 79 | 68 | 36.9 | Yes
```

Notice:
- Screening visit (March 25) is BEFORE consent (April 1) — this is fine for screening
- Baseline visit is ON consent date — also fine
- Blood pressure values are realistic (118/76 and 122/79)
- All visits show Attended = Yes

**adverse_events.csv row:**
```
AE-031 | PT-077 | Headache | Mild | No | 2023-05-10 | 2023-05-12 | 2023-04-01 | Recovered
```

Notice:
- Start date (May 10) is AFTER consent (April 1) ✓
- End date (May 12) is AFTER start date (May 10) ✓
- Severity is filled in ✓
- Is_Serious = No, and Outcome = Recovered (consistent) ✓

---

*This dataset guide is part of the `cdm-trial-validation` beginner portfolio project.*
