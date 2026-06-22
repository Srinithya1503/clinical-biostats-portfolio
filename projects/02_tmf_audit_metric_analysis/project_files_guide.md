# Advanced Excel Operations & Data Reconciliation Manual
**Document ID:** SOP-SPREADSHEET-001  
**Scope:** Manual Audit & Formula Architecture Guide for Cross-Tab TMF Reconciliations

This guide breaks down the structural spreadsheet workflows required to process the raw tracking manifest against the regulatory master reference matrix to build a compliant TMF quality tracker.

---

## 1. Raw Manifest Data Validation
Before initiating calculation formulas, the raw dataset (`synthetic_tmf_manifest.csv`) must be standardized to protect string matching values and date formats.

1.  **Format Columns to Date Format:** Select `Upload_Date` and `Expected_Date` columns, change formatting to `YYYY-MM-DD` (`Short Date` configuration). This prevents computation string errors.
2.  **Ensure Unique String Integrity:** Standardize `Site_ID` (e.g., `SITE-101`) and `Review_Status` (`Approved`, `Rejected`, `Pending`) entries via text alignment trims to eliminate accidental trailing spaces.

---

## 2. Formula Architecture Matrix

### Step 2.1: Calculating the Timeliness Filing Gap
To check if study documentation was checked into the electronic file repository within standard operational windows, calculate the gap days on the **`Reconciled_Audit_Log`** tab:
```excel
=MAX(0, Upload_Date - Expected_Date)

```

*Purpose:* Restricts early or on-time submissions to `0` days, isolating positive numerical values representing filing backlogs.

### Step 2.2: Cross-Tab Regulatory Reference Mapping

To map individual document rows directly to the regulatory criteria stored on the master `DIA_Reference_Map` tab, apply exact-match lookups to find the `Regulatory_Basis` and `Criticality_Level`:

```excel
=VLOOKUP(Artifact_Name, DIA_Reference_Map!$E$3:$K$100, 3, FALSE)

```

### Step 2.3: Generating Dynamic Discrepancy Summaries

To create automated technical notes explaining exact compliance drops per row, combine logical statements inside the summary column:

```excel
=IF(Review_Status="Approved", "No issues identified — document meets all GDP gates.", "CRITICAL ERROR: " & Non_Compliance_Reason & " | Filed " & Timeliness_Gap_Days & " days late.")

```

*Operational Use:* This acts as the automated system notification showing where study documents lack necessary wet/digital signatures, are completely expired, or are incomplete.

---

## 3. Scorecard Aggregation & High-Risk CAPA Filters

### Step 3.1: Building the Site Performance Summary Dashboard

To translate row data observations into site metrics, map your data ranges to a summary grid or construct explicit operational array count constraints:

* **Document Completeness Rate Calculation:** Find the volume of valid, approved materials over total site submissions:
```excel
=COUNTIFS(Reconciled_Audit_Log!$D$2:$D$100, Site_ID, Reconciled_Audit_Log!$L$2:$L$100, "Approved") / COUNTIF(Reconciled_Audit_Log!$D$2:$D$100, Site_ID)

```


* **Process Rejection Rate Calculation:** Extract the frequency of documents failing initial intake audits:
```excel
=COUNTIFS(Reconciled_Audit_Log!$D$2:$D$100, Site_ID, Reconciled_Audit_Log!$L$2:$L$100, "Rejected") / COUNTIF(Reconciled_Audit_Log!$D$2:$D$100, Site_ID)

```



### Step 3.2: Automated Risk Category Triggers

On the **`High_Risk_Sites`** tab, establish automatic classification filters to segregate high-risk entities based on industry regulatory tolerances (<85% compliance):

```excel
=IF(Quality_Pass_Rate_Pct < 85.0, "High Risk - Immediate CAPA Action Required", "Compliant")

```

### Step 3.3: System Polish & Visual Standardization

To format the file for senior leadership reviews, apply clean conditional formatting:

* **High Risk / Alert Triggers:** Apply a light pink fill (`#FFC7CE`) with dark red text (`#9C0006`) to any cell triggering `"High Risk"`.
* **Compliant Baselines:** Apply a soft mint green fill (`#C6EFCE`) with dark green text (`#006100`) for cells validating as `"Compliant"`.
* *Formatting Rule:* Ensure text sizing remains uniform (Calibri/Arial, 10–11pt font size max for data cells) to uphold professional document presentation standards.

---

## 4. Operational Tracker Closeout Workflow

The **`Discrepancy_Query_Log`** is the primary tracking list used by the Project Support Coordinator during daily operations.

1. Apply a **Data Filter** to the master log, isolating only rows marked as `Open` or `Pending Assignment`.
2. Export this extracted list weekly to compile localized communications for regional Clinical Research Associates (CRAs).
3. Upon receipt of corrected, re-signed, or unexpired artifacts from the clinical field site, change the status indicator within the workbook to `Closed`. This automatically updates your dashboard metrics to reflect complete audit readiness.

```

```
