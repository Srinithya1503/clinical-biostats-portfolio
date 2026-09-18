/* ==================================================================
   sas_analysis_basic.sas

   Clinical Trial Benchmarking Analysis - Basic SAS Version

   This script uses only simple, everyday SAS commands:
     - PROC IMPORT   (read the CSV file)
     - DATA step     (clean the data, with plain IF/THEN logic)
     - PROC SORT     (remove duplicates, sort results)
     - PROC FREQ     (count trials by phase / by sponsor)
     - PROC MEANS    (median enrollment, duration statistics)
     - PROC PRINT    (show results in the output window)
     - PROC EXPORT   (save results back to CSV)

   No macros (%let / %macro), no PROC SQL, and no custom functions
   are used, so every step can be read top to bottom.

   BEFORE YOU RUN THIS:
     1. Change the file path on the line below (raw_trials.csv) to
        wherever your file is saved.
     2. Make sure a folder called "results" already exists in that
        same location, since PROC EXPORT will save files into it.
   ================================================================== */


/* ------------------------------------------------------------------
   STEP 1: Read the raw CSV file into a SAS dataset
   ------------------------------------------------------------------ */
proc import datafile="raw_trials.csv"
    out=raw_trials
    dbms=csv
    replace;
    getnames=yes;
    guessingrows=2000;
run;

proc print data=raw_trials (obs=5);
    title "First 5 rows of the raw data";
run;
title;


/* ------------------------------------------------------------------
   STEP 2: Clean the data
     - Fix the phase column (some rows say "NA" or are blank)
     - Fix the sponsor column (blank sponsors become "Unknown")
     - Turn the date text into real SAS dates
       (some dates only have a year and month, like "2007-04",
        so those are treated as the 1st day of that month)
   ------------------------------------------------------------------ */
data clean_trials;
    set raw_trials;

    /* Fix phase */
    if phase = "" or phase = "NA" or phase = "N/A" then phase = "N/A";

    /* Fix sponsor */
    if sponsor_name = "" then sponsor_name = "Unknown";

    /* Fix start_date */
    if length(start_date) = 7 then start_date = trim(start_date) || "-01";
    start_date_clean = input(start_date, yymmdd10.);

    /* Fix completion_date */
    if length(completion_date) = 7 then completion_date = trim(completion_date) || "-01";
    completion_date_clean = input(completion_date, yymmdd10.);

    format start_date_clean completion_date_clean yymmdd10.;

    drop start_date completion_date;
    rename start_date_clean = start_date completion_date_clean = completion_date;
run;

/* Remove duplicate trial IDs, keep the first one found */
proc sort data=clean_trials nodupkey;
    by nct_id;
run;

proc print data=clean_trials (obs=5);
    title "First 5 rows after cleaning";
run;
title;


/* ------------------------------------------------------------------
   STEP 3: Phase distribution (count and percent of trials per phase)
   ------------------------------------------------------------------ */
proc freq data=clean_trials noprint;
    tables phase / out=phase_distribution;
run;

data phase_distribution;
    set phase_distribution;
    trial_count = count;
    percentage = round(percent, 0.01);
    keep phase trial_count percentage;
run;

proc sort data=phase_distribution;
    by descending trial_count;
run;

proc print data=phase_distribution noobs;
    title "Phase Distribution";
run;
title;

proc export data=phase_distribution
    outfile="results/phase_distribution.csv"
    dbms=csv
    replace;
run;


/* ------------------------------------------------------------------
   STEP 4: Top 10 sponsors by number of trials
   ------------------------------------------------------------------ */
proc freq data=clean_trials order=freq noprint;
    tables sponsor_name / out=sponsor_counts;
run;

data top_sponsors;
    set sponsor_counts (obs=10);
    trial_count = count;
    keep sponsor_name trial_count;
run;

proc print data=top_sponsors noobs;
    title "Top 10 Sponsors";
run;
title;

proc export data=top_sponsors
    outfile="results/top_sponsors.csv"
    dbms=csv
    replace;
run;


/* ------------------------------------------------------------------
   STEP 5: Median enrollment by phase
   ------------------------------------------------------------------ */
proc means data=clean_trials noprint median;
    class phase;
    var enrollment_count;
    output out=median_enrollment median=median_enrollment;
run;

data median_enrollment_by_phase;
    set median_enrollment;
    if phase = "" then delete;   /* drop the overall grand-total row */
    keep phase median_enrollment;
run;

proc sort data=median_enrollment_by_phase;
    by descending median_enrollment;
run;

proc print data=median_enrollment_by_phase noobs;
    title "Median Enrollment by Phase";
run;
title;

proc export data=median_enrollment_by_phase
    outfile="results/median_enrollment_by_phase.csv"
    dbms=csv
    replace;
run;


/* ------------------------------------------------------------------
   STEP 6: Trial duration summary by phase (in days)
   ------------------------------------------------------------------ */
data duration_calc;
    set clean_trials;
    if start_date ne . and completion_date ne . then do;
        duration_days = completion_date - start_date;
        if duration_days >= 0 then output;
    end;
run;

proc means data=duration_calc noprint mean median min max n;
    class phase;
    var duration_days;
    output out=trial_duration_summary
        mean=avg_duration_days
        median=median_duration_days
        min=min_duration_days
        max=max_duration_days
        n=trial_count;
run;

data trial_duration_summary;
    set trial_duration_summary;
    if phase = "" then delete;   /* drop the overall grand-total row */
    avg_duration_days = round(avg_duration_days, 0.1);
    keep phase avg_duration_days median_duration_days min_duration_days max_duration_days trial_count;
run;

proc sort data=trial_duration_summary;
    by descending avg_duration_days;
run;

proc print data=trial_duration_summary noobs;
    title "Trial Duration Summary by Phase";
run;
title;

proc export data=trial_duration_summary
    outfile="results/trial_duration_summary.csv"
    dbms=csv
    replace;
run;
