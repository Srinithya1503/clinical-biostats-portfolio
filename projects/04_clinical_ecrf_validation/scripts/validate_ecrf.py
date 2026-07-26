# ==========================================================
# validate_ecrf.py
# Beginner-friendly Clinical Data Validation Script
#
# Reads raw_ecrf_data.csv, checks each row for common CDM data
# quality issues, then writes:
#   - cleaned_ecrf_data.csv        (rows that passed critical checks)
#   - discrepancy_query_log.csv    (a query for every issue found)
#
# ==========================================================

import pandas as pd
from datetime import datetime

raw_df = pd.read_csv("../data/raw_ecrf_data.csv")
print("Raw data loaded. Total rows:", len(raw_df))

# Convert dates so they can be compared
raw_df["Visit_Date_dt"] = pd.to_datetime(raw_df["Visit_Date"], errors="coerce")
raw_df["Consent_Date_dt"] = pd.to_datetime(raw_df["Informed_Consent_Date"], errors="coerce")
today = pd.to_datetime(datetime.today().strftime("%Y-%m-%d"))

query_id_counter = 1     # used to build IDs like Q0001, Q0002...
rows_to_keep = []        # row numbers that pass critical checks
query_list = []          # one dictionary per query found


def add_query(row, form, field, error_type, description, priority):
    global query_id_counter
    query_list.append({
        "Query_ID": "Q" + str(query_id_counter).zfill(4),
        "Site_ID": row["Site_ID"], "Subject_ID": row["Subject_ID"], "Visit": row["Visit"],
        "Form_Name": form, "Field_Name": field, "Error_Type": error_type,
        "Error_Description": description, "Query_Status": "Open", "Priority": priority
    })
    query_id_counter = query_id_counter + 1


# ----------------------------------------------------------
# Loop through every row and apply the validation rules
# ----------------------------------------------------------
for i in range(len(raw_df)):
    row = raw_df.iloc[i]
    row_has_critical_error = False

    # Rule 1: Missing Subject ID (critical - cannot trace the subject)
    if pd.isnull(row["Subject_ID"]):
        row_has_critical_error = True
        add_query(row, "Demographics", "Subject_ID", "Missing Data", "Subject ID field left blank", "High")

    # Rule 2: Missing Visit Date (critical)
    if pd.isnull(row["Visit_Date"]):
        row_has_critical_error = True
        add_query(row, "Visit", "Visit_Date", "Missing Data", "Visit date field left blank", "High")

    # Rule 3: Missing Consent Date (critical)
    if pd.isnull(row["Informed_Consent_Date"]):
        row_has_critical_error = True
        add_query(row, "Informed Consent", "Informed_Consent_Date", "Missing Data", "Consent date not entered", "High")

    # Rule 4: Missing Age (minor - row can still be kept)
    if pd.isnull(row["Age"]):
        add_query(row, "Demographics", "Age", "Missing Data", "Age field not entered by site", "Medium")

    # Rule 5: Missing Weight (minor)
    if pd.isnull(row["Weight_kg"]):
        add_query(row, "Vital Signs", "Weight_kg", "Missing Data", "Weight not recorded at visit", "Medium")

    # Rule 6: Heart Rate outside protocol range (40-180 bpm)
    if row["Heart_Rate_bpm"] > 180 or row["Heart_Rate_bpm"] < 40:
        add_query(row, "Vital Signs", "Heart_Rate_bpm", "Range Check Failure", "Heart rate outside normal range", "High")

    # Rule 7: Systolic Blood Pressure too high (>200 mmHg)
    if row["Systolic_BP_mmHg"] > 200:
        add_query(row, "Vital Signs", "Systolic_BP_mmHg", "Range Check Failure", "Systolic BP exceeds protocol limit", "High")

    # Rule 8: Temperature outside clinical range (34-42 C)
    if pd.notnull(row["Temperature_C"]) and (row["Temperature_C"] > 42 or row["Temperature_C"] < 34):
        add_query(row, "Vital Signs", "Temperature_C", "Range Check Failure", "Temperature outside clinical range", "Medium")

    # Rule 9: Invalid Sex value
    if row["Sex"] not in ["Male", "Female"]:
        add_query(row, "Demographics", "Sex", "Invalid Value", "Sex field contains a non-standard value", "Medium")

    # Rule 10: Missing Investigator Name (minor)
    if pd.isnull(row["Investigator_Name"]):
        add_query(row, "Study Conduct", "Investigator_Name", "Missing Data", "Investigator name not documented", "Low")

    # Rule 11: Visit Date before Consent Date (critical logic error)
    if pd.notnull(row["Visit_Date_dt"]) and pd.notnull(row["Consent_Date_dt"]):
        if row["Visit_Date_dt"] < row["Consent_Date_dt"]:
            row_has_critical_error = True
            add_query(row, "Visit", "Visit_Date", "Logic Check Failure", "Visit date before consent date", "High")

    # Rule 12: Future Visit Date
    if pd.notnull(row["Visit_Date_dt"]) and row["Visit_Date_dt"] > today:
        add_query(row, "Visit", "Visit_Date", "Logic Check Failure", "Visit date entered is in the future", "Medium")

    # Keep the row for the cleaned dataset unless it failed a critical rule
    if row_has_critical_error == False:
        rows_to_keep.append(i)

# ----------------------------------------------------------
# Build and save the cleaned dataset
# ----------------------------------------------------------
cleaned_df = raw_df.loc[rows_to_keep].copy()

cleaned_df["Age"] = cleaned_df["Age"].fillna(cleaned_df["Age"].median())
cleaned_df["Weight_kg"] = cleaned_df["Weight_kg"].fillna(cleaned_df["Weight_kg"].median())
cleaned_df["Investigator_Name"] = cleaned_df["Investigator_Name"].fillna("Unknown")

cleaned_df = cleaned_df.drop(columns=["Visit_Date_dt", "Consent_Date_dt"])
cleaned_df = cleaned_df.drop_duplicates()

cleaned_df.to_csv("../data/cleaned_ecrf_data.csv", index=False)
print("Cleaned data saved. Rows remaining:", len(cleaned_df))

# ----------------------------------------------------------
# Build and save the discrepancy query log
# ----------------------------------------------------------
query_df = pd.DataFrame(query_list)
query_df["Action_Required"] = "Pending site response"
query_df["Query_Date"] = datetime.today().strftime("%Y-%m-%d")
query_df["Resolution_Date"] = ""

query_df.to_csv("../data/discrepancy_query_log.csv", index=False)
print("Discrepancy query log saved. Total queries found:", len(query_df))

print("Validation complete.")
