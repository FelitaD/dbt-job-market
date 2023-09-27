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

![pipeline](docs/job-radar-2.svg)

## Running locally

```bash
streamlit run reporting/home.py
```

## Testing

First, install pytest and required plugins via:

```bash
pip install pytest
pip install -r requirements.txt
```

To run all tests: 

```bash
pytest ./tests
```

_Note: Only streamlit app is tested at the moment, the rest is work in progress._ 





