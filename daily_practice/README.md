# Daily Practice & Applied Coding Log (SAS & R)
This directory logs my consistent, daily programming exercises, algorithmic problem-solving, and implementation micro-tasks. It demonstrates continuous skill development across SAS and R within a clinical data and biostatistics framework.

------------------------------
## 🎯 Purpose & Methodology
In biostatistics and clinical trial programming, writing clean, defensible, and validation-ready code is mandatory. This repository isolates real-world challenges—such as date processing, baseline shifts, safety tables, and survival analysis—using SAS (for data pipeline/CDISC/TLFs) and R (for advanced biostatistical modeling/graphics).

## Core Disciplines Tracked:

* Data Cleaning & Logic Flags: Programmatic handling of clinical anomalies, data truncation, and missing variables.
* CDISC Mapping Logic: Transforming raw clinical trial sources into standardized SDTM/ADaM datasets.
* Statistical Inference & Modeling: Executing and verifying biostatistical tests (t-tests, ANOVA, Kaplan-Meier) across both environments.
* Macro & Function Automation: Building reusable SAS macros and R functions to automate repetitive clinical workflows.

------------------------------
## 📅 30-Day Project-Based Practice Log## Phase 1: Clinical Data Engineering & Base SAS Foundations (Days 1–10)
Target: Read, clean, and structure the raw ONCO-2026 files inside SAS and R.

| Day | Focus Domain | Language | Project Task Description | Target Concept/Output |
|---|---|---|---|---|
| 01 | Data Ingestion | SAS | Write a DATA step with DATALINES to import the raw raw_dm text block. | Card reading / Syntax |
| 02 | Type Conversion | SAS | Convert character strings BRTHDT and RAND_DT into numeric SAS dates. | INPUT() function |
| 03 | Missing Data | R | Import raw_lab into R; flag and isolate missing values (like SUBJ-003 Week 4). | is.na() handling |
| 04 | Sorting & Filtering | SAS | Use PROC SORT on raw_lab to order records by patient and visit chronologically. | BY group sorting |
| 05 | Merging Matrices | SAS | Execute a horizontal MERGE combining raw_dm and raw_lab by patient ID. | Match-merging (IN=) |
| 06 | Data Reshaping | R | Pivot raw_lab from long format to a wide format data frame with distinct visit columns. | tidyr::pivot_wider |
| 07 | Text Normalization | SAS | Use string functions to standardize messy treatment arm text strings to lowercase/uppercase. | UPCASE / STRIP |
| 08 | Clinical Formatting | SAS | Build custom display rules converting sex variables M/F to Male/Female using procedures. | PROC FORMAT |
| 09 | Deduplication | R | Programmatically detect and eliminate duplicate or split-sample lab logs from your matrix. | distinct() filtering |
| 10 | Baseline Isolation | SAS | Subsetting the combined master file to extract only data points marked as Baseline. | First-dot tracking |

------------------------------
## Phase 2: Biostatistical Logic & Hypothesis Testing (Days 11–20)
Target: Execute mathematical calculations and statistical protocols on your structured files.

| Day | Focus Domain | Language | Project Task Description | Target Concept/Output |
|---|---|---|---|---|
| 11 | Deriving Changes | R | Calculate baseline absolute change (CHG) and percent change (PCHG) for tumor metrics. | AVAL - BASE formulas |
| 12 | Summary Statistics | SAS | Compute mean, median, min, max, and variance for baseline biomarker levels. | PROC MEANS reporting |
| 13 | Frequency Tables | SAS | Run demographic balance checks counting patient breakdown metrics across arms. | PROC FREQ counts |
| 14 | Distribution Safety | R | Run Shapiro-Wilk evaluations on biomarker changes to determine mathematical normality. | shapiro.test() plots |
| 15 | Parametric Inference | SAS | Run a two-sample independent t-test comparing biomarker drops in Arm A vs Arm B. | PROC TTEST / p-values |
| 16 | Non-Parametric Path | R | Execute a Mann-Whitney U test on skewed, non-normal lab endpoints. | wilcox.test() analytics |
| 17 | Contingency Analysis | SAS | Perform Fisher's exact verification for treatment groups against safety thresholds. | Chi-Square estimation |
| 18 | Variance Analysis | SAS | Set up a one-way ANOVA tracking marker divergence across three timeline milestones. | PROC ANOVA validation |
| 19 | Linear Modeling | R | Fit a simple linear model predicting patient biomarker response based on baseline age. | lm() regression lines |
| 20 | Survival Modeling | R | Join raw_surv data to build Kaplan-Meier curves tracking death flags across timelines. | survival::survfit |

------------------------------
## Phase 3: Regulatory CDISC Mapping & TLF Generation (Days 21–30)
Target: Transform your dataset into standardized CDISC domains and output submission-grade reports.

| Day | Focus Domain | Language | Project Task Description | Target Concept/Output |
|---|---|---|---|---|
| 21 | CDISC SDTM Build | SAS | Map clean demographic profiles directly into global submission-grade SDTM.DM format. | Domain Compliance |
| 22 | SDTM Lab Mapping | SAS | Transform lab matrices into standard SDTM.LB containing uniform code parameters. | LBTESTCD setting |
| 23 | Date Imputation | R | Code logical date repair procedures assigning standard ISO 8601 strings to messy records. | ISO8601 format string |
| 24 | ADaM Foundations | SAS | Combine your finalized SDTM.DM entries to build a Subject-Level Analysis Dataset. | ADSL construction |
| 25 | ADaM Parameter Build | SAS | Format longitudinal laboratory changes into an analytical ADLB parameter file. | PARAM / PARAMCD |
| 26 | Macro Automation | SAS | Write an automated macro loop generating summary values for multiple lab parameters. | %MACRO / %MEND |
| 27 | Report Structuring | SAS | Design an official baseline demographic table using output systems for layout management. | PROC REPORT layout |
| 28 | Secure Document Export | SAS | Output your clinical baseline demographics table directly into an external secure .rtf file. | ODS RTF template |
| 29 | Log File Review | SAS | Scan, debug, and eliminate hidden errors, notes, or data drops inside compiling program files. | Quality Control / Review |
| 30 | Portfolio Delivery | Markdown | Push all 30 days of linked scripts and code summaries into a single GitHub repository. | Portfolio Finalization |

------------------------------
## Micro-Utility Snippets Directory
This section functions as an active toolbox of reusable snippets used to quickly resolve routine clinical programming snags:
##  Quick-Reference Snippets Index## 1. SAS Missing Value Coalesce (/snippets/sas_missing_handler.sas)
Demonstrates clean usage of the COALESCE and COALESCEC functions to prevent missing value propagation when merging clinical records.

data work.clean_lab;
    set work.merged_lab;
    /* Impute missing current visit with baseline values if missing */
    final_val = coalesce(lab_val, base_val);
run;

## 2. R Time-To-Event Calculator (/snippets/survival_calc.R)
Calculates formal study survival days by parsing ISO dates while handling right-censored patients who survived past data cut-off.

library(lubridate)
calculate_days <- function(rand_dt, last_dt) {
  as.numeric(ymd(last_dt) - ymd(rand_dt))
}

------------------------------



