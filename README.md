# Job Radar 2.0

Version 2 of [Job Radar 1.0](https://github.com/FelitaD/job-radar-1.0) by modifying technologies used.
<br>Focus is emphasized on analytics engineering using [Snowflake](https://www.snowflake.com/en/) coupled with [dbt](https://www.getdbt.com/) 
and visualisations in Looker Studio and Streamlit. Orchestration with Prefect. Data modeling with Data Vault.

## Overview

Add platform architecture.

## Pipelines

### Scrapy crawler - Postgres

- [x] Create crawler container with Docker -> commits on old branch `revamp-crawler`
- [ ] Create glassdoor spider

### Postgres - Snowflake

- [x] [Migrate Postgres to Snowflake](https://github.com/FelitaD/Learning-in-Public/blob/main/Databases/Data%20Lakes%20%26%20Data%20Warehouses/Snowflake/Migrate%20Postgres%20to%20Snowflake.md)

### dbt - Snowflake

- [x] Processing in Snowflake with dbt

### Snowflake - Looker Studio / Streamlit

- [x] Looker report
- [ ] Streamlit app

### Prefect

- [ ] Orchestrate project

### Data Vault 2.0

- [ ] Create data model

