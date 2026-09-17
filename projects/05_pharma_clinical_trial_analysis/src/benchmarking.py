"""
Benchmarking module.
Computes aggregated metrics from the cleaned clinical trial
DataFrame: phase distribution, top sponsors, enrollment medians per
phase, and trial duration statistics.
"""

import logging


class PipelineBenchmarker:
    """
    Generates benchmarking metrics from a cleaned clinical trials
    DataFrame produced by TrialDataParser.
    """

    def __init__(self, dataframe):
        self.df = dataframe.copy()
        self.logger = logging.getLogger(self.__class__.__name__)

    def get_phase_distribution(self):
        """
        Returns a DataFrame with the count and percentage of trials
        for each trial phase.
        """
        self.logger.info("Calculating phase distribution...")

        phase_counts = self.df["phase"].value_counts().reset_index()
        phase_counts.columns = ["phase", "trial_count"]

        total = phase_counts["trial_count"].sum()
        phase_counts["percentage"] = (
            phase_counts["trial_count"] / total * 100
        ).round(2)

        return phase_counts

    def get_top_sponsors(self, top_n=10):
        """
        Returns a DataFrame with the top N sponsors ranked by number
        of trials.
        """
        self.logger.info("Calculating top %d sponsors...", top_n)

        sponsor_counts = (
            self.df["sponsor_name"].value_counts().head(top_n).reset_index()
        )
        sponsor_counts.columns = ["sponsor_name", "trial_count"]

        return sponsor_counts

    def get_median_enrollment_by_phase(self):
        """
        Returns a DataFrame with the median enrollment count grouped
        by trial phase.
        """
        self.logger.info("Calculating median enrollment by phase...")

        grouped = (
            self.df.groupby("phase")["enrollment_count"].median().reset_index()
        )
        grouped.columns = ["phase", "median_enrollment"]
        grouped = grouped.sort_values("median_enrollment", ascending=False)

        return grouped

    def get_trial_duration_summary(self):
        """
        Calculates trial duration in days (completion_date minus
        start_date) and returns summary statistics grouped by phase.
        """
        self.logger.info("Calculating trial duration metrics...")

        duration_df = self.df.copy()
        duration_df["duration_days"] = (
            duration_df["completion_date"] - duration_df["start_date"]
        ).dt.days

        duration_df = duration_df[duration_df["duration_days"].notna()]
        duration_df = duration_df[duration_df["duration_days"] >= 0]

        summary = (
            duration_df.groupby("phase")["duration_days"]
            .agg(["mean", "median", "min", "max", "count"])
            .reset_index()
        )

        summary.columns = [
            "phase",
            "avg_duration_days",
            "median_duration_days",
            "min_duration_days",
            "max_duration_days",
            "trial_count",
        ]

        summary["avg_duration_days"] = summary["avg_duration_days"].round(1)

        return summary

    def run_all_benchmarks(self):
        """
        Runs every benchmarking method and returns the results as a
        dictionary of DataFrames, keyed by metric name.
        """
        self.logger.info("Running full benchmarking suite...")

        results = {
            "phase_distribution": self.get_phase_distribution(),
            "top_sponsors": self.get_top_sponsors(),
            "median_enrollment_by_phase": self.get_median_enrollment_by_phase(),
            "trial_duration_summary": self.get_trial_duration_summary(),
        }

        self.logger.info("Benchmarking suite complete.")
        return results
