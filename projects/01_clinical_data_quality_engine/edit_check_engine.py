"""
edit_check_engine.py
-------------
This is the VALIDATION ENGINE -- the most important file in the project.

It reads the three CSV files created by generate_data.py and checks
each record for errors. When it finds a problem, it writes a "query"
to a report file called issues_found.csv.

"""

import os
import sys

import pandas as pd


# ── Step 1: Load the data ────────────────────────────────────────────────────

def load_data():
   
    files_needed = [
        "data/patients.csv",
        "data/visits.csv",
        "data/adverse_events.csv",
    ]

    for filepath in files_needed:
        if not os.path.exists(filepath):
            print(f"ERROR: Could not find '{filepath}'")
            print("Please run:  python generate_data.py  first.")
            sys.exit(1)

    patients = pd.read_csv("data/patients.csv")
    visits   = pd.read_csv("data/visits.csv")
    ae       = pd.read_csv("data/adverse_events.csv")

    print(f"  Loaded {len(patients)} patients, "
          f"{len(visits)} visits, "
          f"{len(ae)} adverse events.")

    return patients, visits, ae


# ── Step 2: Define a helper function ─────────────────────────────────────────

def make_issue(patient_id, visit, field, value, check_id, severity, message):
   
    return {
        "Patient_ID":    patient_id,
        "Visit":         visit,
        "Field":         field,
        "Current_Value": str(value),
        "Check_ID":      check_id,
        "Severity":      severity,
        "Query_Message": message,
    }


# ── Step 3: The Checks ───────────────────────────────────────────────────────
# Each check is its own function.
# Every function returns a LIST of issues found.
# An empty list [] means no problems were found by that check.


# --- CHECK 1: Age must be between 18 and 80 ---

def check_age(patients):
    issues = []

    for _, row in patients.iterrows():
        age = row["Age"]

        # Check if age is outside the allowed range
        if not (18 <= age <= 80):
            issues.append(make_issue(
                patient_id = row["Patient_ID"],
                visit      = "N/A (Patient Record)",
                field      = "Age",
                value      = age,
                check_id   = "CHK-01",
                severity   = "Critical",
                message    = (
                    f"CHK-01: Patient age is {age}, which is outside the "
                    f"allowed range of 18 to 80 years. "
                    f"Please verify the date of birth and correct."
                ),
            ))

    return issues


# --- CHECK 2: Male patients should not have pregnancy test marked "Yes" ---

def check_pregnancy_test_gender(patients):
    issues = []

    for _, row in patients.iterrows():
        if row["Gender"] == "Male" and row["Pregnancy_Test_Done"] == "Yes":
            issues.append(make_issue(
                patient_id = row["Patient_ID"],
                visit      = "N/A (Patient Record)",
                field      = "Pregnancy_Test_Done",
                value      = f"Gender={row['Gender']}, Test={row['Pregnancy_Test_Done']}",
                check_id   = "CHK-02",
                severity   = "Major",
                message    = (
                    f"CHK-02: Patient is recorded as Male but Pregnancy Test "
                    f"is marked 'Yes'. These fields contradict each other. "
                    f"Please check if the gender or the test field is incorrect."
                ),
            ))

    return issues


# --- CHECK 3: Blood pressure must be in a realistic range ---

def check_blood_pressure(visits):
    issues = []

    for _, row in visits.iterrows():
        sbp = row["Systolic_BP"]
        dbp = row["Diastolic_BP"]

        # Check systolic (top number)
        if not (60 <= sbp <= 250):
            issues.append(make_issue(
                patient_id = row["Patient_ID"],
                visit      = row["Visit_Name"],
                field      = "Systolic_BP",
                value      = sbp,
                check_id   = "CHK-03",
                severity   = "Critical",
                message    = (
                    f"CHK-03: Systolic blood pressure is {sbp} mmHg at "
                    f"{row['Visit_Name']}. This is outside the realistic "
                    f"range of 60-250 mmHg. Please verify the measurement."
                ),
            ))

        # Check diastolic (bottom number)
        if not (30 <= dbp <= 150):
            issues.append(make_issue(
                patient_id = row["Patient_ID"],
                visit      = row["Visit_Name"],
                field      = "Diastolic_BP",
                value      = dbp,
                check_id   = "CHK-03",
                severity   = "Critical",
                message    = (
                    f"CHK-03: Diastolic blood pressure is {dbp} mmHg at "
                    f"{row['Visit_Name']}. This is outside the realistic "
                    f"range of 30-150 mmHg. Please verify the measurement."
                ),
            ))

        # Check that diastolic is NOT higher than systolic
        if dbp >= sbp:
            issues.append(make_issue(
                patient_id = row["Patient_ID"],
                visit      = row["Visit_Name"],
                field      = "Diastolic_BP / Systolic_BP",
                value      = f"SBP={sbp}, DBP={dbp}",
                check_id   = "CHK-03B",
                severity   = "Critical",
                message    = (
                    f"CHK-03B: Diastolic BP ({dbp}) is equal to or higher "
                    f"than Systolic BP ({sbp}) at {row['Visit_Name']}. "
                    f"This is physically impossible. Please check both values."
                ),
            ))

    return issues


# --- CHECK 4: Visit date must NOT be before consent date ---

def check_visit_before_consent(visits):
    issues = []

    for _, row in visits.iterrows():

        # Skip the screening visit -- that one CAN happen before full consent
        if row["Visit_Name"] == "Screening":
            continue

        visit_date   = pd.to_datetime(row["Visit_Date"])
        consent_date = pd.to_datetime(row["Consent_Date"])

        if visit_date < consent_date:
            issues.append(make_issue(
                patient_id = row["Patient_ID"],
                visit      = row["Visit_Name"],
                field      = "Visit_Date",
                value      = f"Visit={row['Visit_Date']}, Consent={row['Consent_Date']}",
                check_id   = "CHK-04",
                severity   = "Critical",
                message    = (
                    f"CHK-04: The visit '{row['Visit_Name']}' on "
                    f"{row['Visit_Date']} happened BEFORE the patient "
                    f"signed consent on {row['Consent_Date']}. "
                    f"This is a GCP violation. Both dates must be reviewed "
                    f"and a protocol deviation form may be required."
                ),
            ))

    return issues


# --- CHECK 5: Side effect dates must be in order ---

def check_ae_dates(ae):
    issues = []

    for _, row in ae.iterrows():

        start_date   = pd.to_datetime(row["Start_Date"])
        end_date     = pd.to_datetime(row["End_Date"])
        consent_date = pd.to_datetime(row["Consent_Date"])

        # Check: end date must not be before start date
        if end_date < start_date:
            issues.append(make_issue(
                patient_id = row["Patient_ID"],
                visit      = "Adverse Event",
                field      = "End_Date",
                value      = f"Start={row['Start_Date']}, End={row['End_Date']}",
                check_id   = "CHK-05A",
                severity   = "Major",
                message    = (
                    f"CHK-05A: Side effect '{row['Side_Effect']}' "
                    f"(AE #{row['AE_Number']}) has an end date "
                    f"({row['End_Date']}) that is BEFORE its start date "
                    f"({row['Start_Date']}). Please check for a date typo."
                ),
            ))

        # Check: side effect cannot start before consent
        if start_date < consent_date:
            issues.append(make_issue(
                patient_id = row["Patient_ID"],
                visit      = "Adverse Event",
                field      = "Start_Date",
                value      = f"AE Start={row['Start_Date']}, Consent={row['Consent_Date']}",
                check_id   = "CHK-05B",
                severity   = "Critical",
                message    = (
                    f"CHK-05B: Side effect '{row['Side_Effect']}' "
                    f"(AE #{row['AE_Number']}) started on {row['Start_Date']}, "
                    f"which is BEFORE the patient joined the trial "
                    f"({row['Consent_Date']}). This may be a pre-existing "
                    f"condition that was wrongly recorded as a trial side effect."
                ),
            ))

    return issues


# --- CHECK 6: Fatal events MUST be marked as Serious ---

def check_fatal_must_be_serious(ae):
    issues = []

    for _, row in ae.iterrows():
        if row["Outcome"] == "Fatal" and row["Is_Serious"] != "Yes":
            issues.append(make_issue(
                patient_id = row["Patient_ID"],
                visit      = "Adverse Event",
                field      = "Is_Serious",
                value      = f"Outcome={row['Outcome']}, Serious={row['Is_Serious']}",
                check_id   = "CHK-06",
                severity   = "Critical",
                message    = (
                    f"CHK-06: URGENT -- Side effect '{row['Side_Effect']}' "
                    f"(AE #{row['AE_Number']}) has Outcome='Fatal' but is "
                    f"NOT marked as Serious. A fatal event is ALWAYS serious "
                    f"per ICH E2A. Please correct Is_Serious to 'Yes' "
                    f"immediately and check if a 7-day safety report is needed."
                ),
            ))

    return issues


# --- CHECK 7: Serious events must have a severity filled in ---

def check_serious_needs_severity(ae):
    issues = []

    for _, row in ae.iterrows():
        severity_value = str(row["Severity"]).strip()

        if row["Is_Serious"] == "Yes" and severity_value == "":
            issues.append(make_issue(
                patient_id = row["Patient_ID"],
                visit      = "Adverse Event",
                field      = "Severity",
                value      = f"Is_Serious={row['Is_Serious']}, Severity=[BLANK]",
                check_id   = "CHK-07",
                severity   = "Major",
                message    = (
                    f"CHK-07: Side effect '{row['Side_Effect']}' "
                    f"(AE #{row['AE_Number']}) is marked as Serious but the "
                    f"Severity field is blank. All Serious events must have a "
                    f"severity grade (Mild/Moderate/Severe). Please complete."
                ),
            ))

    return issues


# ── Step 4: Run all checks and combine results ───────────────────────────────

def run_all_checks(patients, visits, ae):
    """
    This function runs every check and combines all the issues into one list.
    It also prints progress updates as it goes.
    """

    print()
    print("Running validation checks...")
    print()

    all_issues = []

    # Run each check and collect the issues it finds
    # We print how many issues each check found

    results = check_age(patients)
    print(f"  CHK-01 Age range check          --> {len(results):>4} issues found")
    all_issues.extend(results)

    results = check_pregnancy_test_gender(patients)
    print(f"  CHK-02 Gender/pregnancy check   --> {len(results):>4} issues found")
    all_issues.extend(results)

    results = check_blood_pressure(visits)
    print(f"  CHK-03 Blood pressure check     --> {len(results):>4} issues found")
    all_issues.extend(results)

    results = check_visit_before_consent(visits)
    print(f"  CHK-04 Visit before consent     --> {len(results):>4} issues found")
    all_issues.extend(results)

    results = check_ae_dates(ae)
    print(f"  CHK-05 Adverse event dates      --> {len(results):>4} issues found")
    all_issues.extend(results)

    results = check_fatal_must_be_serious(ae)
    print(f"  CHK-06 Fatal = Serious check    --> {len(results):>4} issues found")
    all_issues.extend(results)

    results = check_serious_needs_severity(ae)
    print(f"  CHK-07 Serious needs severity   --> {len(results):>4} issues found")
    all_issues.extend(results)

    return all_issues


# ── Step 5: Print a summary and save results ─────────────────────────────────

def print_summary(all_issues, total_records):
    """
    Print a clean summary of what we found to the terminal.
    """
    total_issues = len(all_issues)

    print()
    print("=" * 55)
    print("  RESULTS SUMMARY")
    print("=" * 55)

    if total_issues == 0:
        print("  No issues found! The data looks clean.")
        return

    print(f"  Total records checked : {total_records:>6,}")
    print(f"  Total issues found    : {total_issues:>6,}")

    # Count by severity
    issues_df = pd.DataFrame(all_issues)
    severity_counts = issues_df["Severity"].value_counts()

    print()
    print("  Issues by severity:")
    for level in ["Critical", "Major", "Minor"]:
        count = severity_counts.get(level, 0)
        print(f"    {level:<10}: {count:>4}")

    print()
    print("  Issues by check:")
    check_counts = issues_df["Check_ID"].value_counts().sort_index()
    for check_id, count in check_counts.items():
        print(f"    {check_id}: {count:>4} issues")

    print()
    print("  Top 5 patients with most issues:")
    top_patients = (
        issues_df.groupby("Patient_ID")
        .size()
        .sort_values(ascending=False)
        .head(5)
    )
    for patient_id, count in top_patients.items():
        print(f"    {patient_id}: {count} issues")

    print("=" * 55)


# ── MAIN: Run the whole engine ───────────────────────────────────────────────

def main():
    print("=" * 55)
    print("  Clinical Data Validation Engine")
    print("  Reading data and checking for errors...")
    print("=" * 55)

    # Load the data files
    patients, visits, ae = load_data()

    # Count the total number of records checked
    total_records = len(patients) + len(visits) + len(ae)

    # Run all the checks
    all_issues = run_all_checks(patients, visits, ae)

    # Save the results to a CSV file
    if all_issues:
        results_df = pd.DataFrame(all_issues)
        results_df.to_csv("issues_found.csv", index=False)
        print()
        print(f"  Issues saved to: issues_found.csv")
    else:
        print()
        print("  No issues found. No output file created.")

    # Print the summary to the terminal
    print_summary(all_issues, total_records)

    print()
    print("  Next: Open 'issues_found.csv' to review all the queries.")
    print()


if __name__ == "__main__":
    main()
