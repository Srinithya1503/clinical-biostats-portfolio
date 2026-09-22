/* =================================================================================================
   =================================================================================================
               CLINICAL TRIAL DATA ANALYSIS - PRACTICE SELF ASSESSMENT (BASE SAS)
   ==================================================================================================
   ================================================================================================== */

/* =====================================================================
   MODULE 1 - Advanced Clinical SAS Data Manipulation and Functions
   ===================================================================== */


/* =====================================================================
   1.1 Data Extraction
   ===================================================================== */

/* 1. Define the SAS Library */

LIBNAME clinases "C:\Users\srinithya\Desktop\Clinical_SAS\assessment\clinases";

/* 2. Import Sheet 1 (raw_clinical) */

PROC IMPORT OUT = clinases.raw_clinical
            DATAFILE = "C:\Users\srinithya\Desktop\Clinical_SAS\assessment\clinases\clinical_trials.xlsx"
            DBMS = EXCEL REPLACE;
            SHEET = "raw_clinical";
            GETNAMES = YES;
            RUN;

PROC PRINT; RUN;


/* 3.Import Sheet 2 (lab_results) */

PROC IMPORT
            DATAFILE = "C:\Users\srinithya\Desktop\Clinical_SAS\assessment\clinases\clinical_trials.xlsx"
            DBMS = EXCEL
            REPLACE;
            OUT = clinases.lab_results;
            SHEET = "lab_results";
            GETNAMES = YES;
            RUN;

PROC PRINT; RUN;


/* 4. Verify Data Structures with PROC CONTENTS */

PROC CONTENTS DATA = clinases.raw_clinical;
 TITLE "Metadata and variable types for raw clinical data";
RUN;
TITLE;

PROC CONTENTS DATA = clinases.lab_results;
 TITLE "Metadata and variable types for lab results";
RUN;
TITLE;


/* =====================================================================
   1.2 Character Manipulation
   ===================================================================== */

DATA cleaned_data;
   RETAIN first_name last_name FULL_NAME phone_no PHONE_CLEAN;
   SET clinases.raw_clinical;
  /* 1. Combine last_name and first_name in 'LASTNAME, FIRSTNAME' format */
  FULL_NAME = UPCASE(COMPBL(CATX(', ', last_name, first_name)));
  /* 2. Strip all non-numeric characters from phone_no */
  PHONE_CLEAN = COMPRESS(phone_no, , 'kd');
RUN;

/* 3. Print the first 10 rows side-by-side to verify */
PROC PRINT DATA=cleaned_data(OBS=10);
TITLE "Verification of Name Combination and Phone Number Cleaning";

RUN;



/* =====================================================================
   1.3 Type Conversion
   ===================================================================== */

DATA converted_data;
    SET cleaned_data;
     /* 1. Convert numeric site_id_num to character SITE_ID. Adjust '8.' to match the expected maximum width of your site IDs
        and -l modifier to left-aligns the resulting character string, removing any leading spaces. */
    SITE_ID = PUT(site_id_num, 8., -1);
    /* 2. Convert character dob_str ('DDMMYYYY') to true SAS date DOB */
    DOB = INPUT(dob_str, DDMMYY8.);
    FORMAT DOB Date9.;
RUN;

PROC PRINT DATA=converted_datal(OBS=10);
VAR site_id_num SITE_ID dob_str DOB;
TITLE "Verification of Site ID and DOB Datatype";
RUN;
TITLE;

/* =====================================================================
   1.4 Date and Numeric Functions
   ===================================================================== */

DATA calculated_data;
   SET converted_datal;
   /* 1. Calculate subject AGE in years using YRDIF with 'AGE' basis */

   AGE = YRDIF(DOB, visit_date, 'AGE');
   /* 2. Calculate TOTAL_DOSE using the SUM function to handle missing values safely */
   TOTAL_DOSE = SUM(base_dose, booster_dose);
RUN;

/* Quick verification print */

PROC PRINT DATA=calculated_datal(obs=10);

 VAR DOB visit_date AGE base_dose booster_dose TOTAL_DOSE;

 TITLE "Verification of Age and Total Dose Calculations";

RUN;
TITLE;

/*

3. COMPARISON ANALYSIS


If a subject has a missing booster_dose (represented  '.' in SAS) :

- Using the '+' operator (base_dose + booster_dose):

SAS strict arithmetic rules state that adding any numeric value to a missing value results in a missing  

value, Therefore, TOTAL_DOSE would become missing (.), completely ignoring the valid base_dose data.
Additionally, SAS will write a "Missing values were generated" note to the log.

- Using the SUM() function (sum(base_dose, booster_dose)):
The SUM function automatically ignores missing values and calculates the total based entirely on remaining
non-missing arguments.The subject's TOTAL_DOSE will safely equal their base_dose,and no warning logs will be triggered.
*/

/* =====================================================================
   1.5 Conditional Logic
   ===================================================================== */

DATA classified_data;
    SET calculated_data;

    /* 1. Categorize DOSE_GROUP using conditional logic

    Explicitly handling missing values prevents them from accidentally falling into the 'Low' tier */
    IF TOTAL_DOSE < 75 THEN DOSE_GROUP = 'Low';
    ELSE IF TOTAL_DOSE <=125 THEN DOSE_GROUP = 'Medium';
    ELSE IF TOTAL_DOSE > 125 THEN DOSE_GROUP = 'High';
    ELSE DOSE_GROUP = 'NA';

   /* 2. Allocate SAFETY_STIPEND based on the categorized groups */
   IF DOSE_GROUP = 'Low' THEN SAFETY_STIPEND = 25;
   ELSE IF DOSE_GROUP = 'Medium' THEN SAFETY_STIPEND = 50;
   ELSE IF DOSE_GROUP = 'High' THEN SAFETY_STIPEND = 75;
   ELSE SAFETY_STIPEND = .;

  /* Apply the DOLLAR8.2 display format */
  FORMAT SAFETY_STIPEND DOLLAR8.2;
RUN;

/* 3. Generate a freuency table to confirm tier populations */
PROC FREQ DATA=classified_data;
   TABLES DOSE_GROUP;
   TITLE "Frequency Distribution of Dose Groups and Tiers";
RUN;
TITLE;


/* =====================================================================
   1.6 Dataset Structuring
   ===================================================================== */

/* 1. Finalize the structure, order, and formatting of the dataset */


DATA clinases.clinical_final (KEEP = subjid FULL_NAME SITE_ID DOB AGE TOTAL_DOSE DOSE_GROUP SAFETY_STIPEND ae_status bmi);
  RETAIN subjid FULL_NAME SITE_ID DOB AGE TOTAL_DOSE DOSE_GROUP SAFETY_STIPEND ae_status bmi;
  SET classified_data;

  /* 2. Apply permanent visual display formats */
  FORMAT DOB DATE9. SAFETY_STIPEND DOLLAR8.2;
RUN;

/* 3. Print the full structural metadata report */
PROC CONTENTS DATA=clinases.clinical_final varnum;
  TITLE "Metadata and variable position report for clinical_final";
RUN;
TITLE;





































