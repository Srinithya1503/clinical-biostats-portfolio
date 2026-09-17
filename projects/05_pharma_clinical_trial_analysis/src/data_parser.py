"""
Data Parser module.
Responsible for flattening the nested JSON study records returned by
the ClinicalTrials.gov API into a clean, tabular pandas DataFrame.
"""

import logging

import pandas as pd


class TrialDataParser:
    """
    Parses raw JSON study records into a flat pandas DataFrame with
    the fields required for benchmarking analysis: NCT ID, title,
    sponsor, phase, status, dates, enrollment, and interventions.
    """

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def parse_studies(self, studies):
        """
        Takes a list of raw study dictionaries and returns a flat
        pandas DataFrame, one row per study.
        """
        self.logger.info("Parsing %d raw study records...", len(studies))
        rows = []

        for study in studies:
            try:
                row = self._parse_single_study(study)
                rows.append(row)
            except Exception as error:
                self.logger.warning(
                    "Skipping a study due to a parsing error: %s", error
                )
                continue

        df = pd.DataFrame(rows)
        self.logger.info("Parsing complete. Produced %d rows.", len(df))
        return df

    def _parse_single_study(self, study):
        """
        Flattens a single nested study record into a plain dictionary
        of the fields we care about.
        """
        protocol = study.get("protocolSection", {})

        identification = protocol.get("identificationModule", {})
        status_module = protocol.get("statusModule", {})
        sponsor_module = protocol.get("sponsorCollaboratorsModule", {})
        design_module = protocol.get("designModule", {})
        interventions_module = protocol.get("armsInterventionsModule", {})

        nct_id = identification.get("nctId", "")
        brief_title = identification.get("briefTitle", "")

        lead_sponsor = sponsor_module.get("leadSponsor", {})
        sponsor_name = lead_sponsor.get("name", "Unknown")

        overall_status = status_module.get("overallStatus", "Unknown")

        start_date_struct = status_module.get("startDateStruct", {})
        start_date = start_date_struct.get("date", "")

        completion_date_struct = status_module.get("completionDateStruct", {})
        completion_date = completion_date_struct.get("date", "")

        phases = design_module.get("phases", [])
        phase = phases[0] if phases else "N/A"

        enrollment_info = design_module.get("enrollmentInfo", {})
        enrollment_count = enrollment_info.get("count", None)

        interventions_list = interventions_module.get("interventions", [])
        intervention_names = [item.get("name", "") for item in interventions_list]
        interventions_str = "; ".join(intervention_names)

        row = {
            "nct_id": nct_id,
            "brief_title": brief_title,
            "sponsor_name": sponsor_name,
            "phase": phase,
            "overall_status": overall_status,
            "start_date": start_date,
            "completion_date": completion_date,
            "enrollment_count": enrollment_count,
            "interventions": interventions_str,
        }
        return row

    def clean_data(self, df):
        """
        Cleans the flat DataFrame: fixes numeric and date types,
        handles missing values, and removes duplicate NCT IDs.
        """
        self.logger.info("Cleaning parsed data...")

        clean_df = df.copy()

        clean_df["enrollment_count"] = pd.to_numeric(
            clean_df["enrollment_count"], errors="coerce"
        )

        clean_df["start_date"] = pd.to_datetime(
            clean_df["start_date"], errors="coerce"
        )
        clean_df["completion_date"] = pd.to_datetime(
            clean_df["completion_date"], errors="coerce"
        )

        clean_df["phase"] = clean_df["phase"].fillna("N/A")
        clean_df["sponsor_name"] = clean_df["sponsor_name"].fillna("Unknown")

        clean_df = clean_df.drop_duplicates(subset=["nct_id"])

        self.logger.info(
            "Cleaning complete. %d rows remain after cleaning.", len(clean_df)
        )
        return clean_df
