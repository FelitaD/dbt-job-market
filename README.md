<h1 align="center">
    Job Radar 2.0
</h1>

<p align="center">
    <strong>🎯&nbsp; A web app to search and compare data engineer jobs 👷‍♀️</strong>
</p>

<p align="center">
    <a href="https://job-radar.streamlit.app/"><img src="https://static.streamlit.io/badges/streamlit_badge_black_white.svg"></a>
</p>

Ingest, process and visualize job listings from 2 websites ([Welcome To The Jungle](https://www.welcometothejungle.com/) 
and [Linkedin](https://www.linkedin.com/jobs/)). Job Radar 2.0 offers more possibilities than these websites to filter jobs: 
technologies asked for the role, company statistics from Glassdoor and comparison to other jobs.  
Refactored version of [Job Radar 1.0](https://github.com/FelitaD/job-radar-1.0) with desire to try new technologies:
- _Orchestration_: Airflow &rarr; Prefect
- _Storage_: PostgreSQL &rarr; Snowflake / BigQuery
- _Processing_: Python &rarr; dbt
- _Visualization_: REST API &rarr; Looker Studio / Streamlit

****

## Pipeline overview

<p align="center">
    <img src="docs/job-radar-2.svg" width=600>
</p>

  
## Tranformation: data lineage

![data_lineage](/Users/donor/PycharmProjects/job-radar-2.0/docs/data_lineage.png)

- The first and main step of the transformation is to extract technologies from jobs descriptions.
In the table `jobs` only those that have a technology (from `base_keywords`) are present.
- For these relevant jobs, the `companies`' information is extracted from Glassdoor.
- Multiple `scores` are calculated such as seniority, rating, relevancy.
- Finally, the `sankey_data` table shows how the original data (`raw_job_postings`) is kept in each transformation categories.

## Running pipeline with Prefect deployment

```bash
python3 orchestration/ingestion_flow.py
```

## Running web app locally

```bash
streamlit run home.py
```

## Testing & Documentation

To run all tests: 

```bash
pytest ./tests
```

To create coverage report:

```bash
coverage run --source=. --omit='tests/*','__init__.py' -m pytest
coverage report
```
Generate a badge:

```bash
coverage-badge -o coverage.svg
```

To create docstring coverage report:
```bash

```
The options will skip init files, include present docstrings, exclude pattern and create a badge.

## TODO

- [x] Add timeline
- [x] Add notes in Streamlit
- [x] Improve charts layout
- [ ] Complete all tests
- [x] Create test coverage badge 
- [ ] Complete all docstrings
- [x] Create docstring coverage badge 
- [ ] Add missing documentation in dbt
- [ ] Add code style black
- [ ] Improve CI/CD
- [ ] Improve dbt best practices
- [ ] Improve prefect best practices
- [ ] Add CDC
