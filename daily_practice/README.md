# Daily Practice & Applied Coding Log

This directory logs my consistent, daily programming exercises, algorithmic problem-solving, and implementation micro-tasks. It demonstrates continuous skill development across **SQL, Python, SAS, and R** within a clinical data framework.

---

##  Purpose & Methodology

In clinical data analytics and statistical programming, writing clean, defensible, and efficient code requires continuous refinement. The exercises in this folder isolate real-world data challenges—such as date calculations, mapping structures, and baseline changes—outside of broad, production-grade projects.

### Core Disciplines Tracked:
* **Data Cleaning & Logic Flags:** Programmatic handling of clinical anomalies, data truncation, and missing variables.
* **CDISC Mapping Logic:** Hard-coded practice transformations from raw sources to standardized SDTM/ADaM variables.
* **Statistical Logic Testing:** Verifying mathematical calculations (e.g., changes from baseline, risk ratios) via multiple languages.
* **Macro & Utility Automation:** Building small, highly reusable templates to speed up repetitive data-processing workflows.

---

## Practice Activity Log

| Day Log | Focus Domain | Language | Task Description | Target Variable/Concept |
| :--- | :--- | :--- | :--- | :--- |
| **Week 01** | Clinical Data Management | Python | Parsing messy string-based lab results into uniform floats using Regex. | Data Normalization |
| **Week 02** | Base SAS / Macros | SAS | Designing a reusable macro to calculate chronological age from `BRTHDT` and `RFSTDTC`. | ISO 8601 Date Parsing |
| **Week 03** | Clinical SAS / SQL | PROC SQL | Executing complex overlapping joins to find Adverse Events occurring within 30 days of study drug discontinuation. | Event Windows |
| **Week 04** | Biostatistics Logic | Python / R | Creating an automated script to compute Baseline Change (`CHG` and `PCHG`) across varied post-baseline visits. | `AVAL`, `BASE`, `CHG` |
| **Week 05** | CDISC Standards | SAS | Manually constructing an SDTM `DM` (Demographics) domain snippet from raw, unstructured clinical arrays. | Domain Structure |
| **Week 06** | Healthcare Analytics | SQL | Building an analytics query to parse longitudinal inpatient electronic health records into distinct hospital stay episodes. | Data Windowing |
| **Week 07** | Text Mining / NLP | Python | Extracting inclusion/exclusion checklist points from semi-structured clinical document logs. | String Parsing |


---

##  Execution & Testing
All scripts stored in this directory are fully self-contained. They utilize synthesized mock data structures embedded directly within the code (e.g., hard-coded data steps in SAS or dictionary arrays in Python) so they can be run instantly without relying on external file structures.

To test any file on your local machine, run:
```bash
# Example for testing a Python day-practice script
python daily_practice/day01_lab_parser.py
```
