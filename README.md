# Job Radar 2.0

Version 2 of [Job Radar 1.0](https://github.com/FelitaD/job-radar-1.0) by modifying technologies used.
<br>Focus is emphasized on analytics engineering using [Snowflake](https://www.snowflake.com/en/) coupled with [dbt](https://www.getdbt.com/) 
and visualisations in Looker Studio and Streamlit. Orchestration with Prefect. Data modeling with Data Vault.

## Overview

Add platform architecture.

## Components

### Scrapy crawler

- [x] Create crawler container with Docker -> commits on old branch `revamp-crawler`
- [x] Add analytics engineer research term to wttj spider

### Octoparse

- [x] Linkedin eu remote
- [ ] Linkedin fr hybrid
- [ ] Glassdoor companies

### Postgres

- [x] Add table companies

### Fivetran

- [ ] Set up Postgres connector with reverse SSH on ec2 instance
- [ ] Add other connectors
 
### Snowflake

- [x] [Migrate Postgres to Snowflake](https://github.com/FelitaD/Learning-in-Public/blob/main/Databases/Data%20Lakes%20%26%20Data%20Warehouses/Snowflake/Migrate%20Postgres%20to%20Snowflake.md)
- [ ] Add created_at in stage

### dbt

- [x] Process technos
- [ ] Create table for streamlit: techno stack, rename columns
- [ ] Process location
- [ ] Add production deployment

### Looker Studio

- [x] Looker report
- [ ] Streamlit app

### Streamlit

- [ ] Search for keywords flat hierarchy, flexible hours

### Prefect

- [ ] Orchestrate project

### Data Vault 2.0

- [ ] Create data model

