# Job Radar 2.0

Improve [Job Radar 1.0](https://github.com/FelitaD/job-radar-1.0) by modifying technologies used.
<br>Focus is emphasized on analytics engineering using [dbt](https://www.getdbt.com/) and [Snowflake](https://www.snowflake.com/en/).

## Roadmap

- [x] [Migrate Postgres to Snowflake](https://github.com/FelitaD/Learning-in-Public/blob/main/Databases/Data%20Lakes%20%26%20Data%20Warehouses/Snowflake/Migrate%20Postgres%20to%20Snowflake.md)

- [x] Processing in Snowflake with dbt

- [x] Create crawler container with Docker
- [ ] Save playwright links to volume

```commandline
docker build --no-cache -t scrapy-docker . 
docker run -i --env-file ./config/.env --mount source=playwright_links,target=/app/playwright_links scrapy-docker
```
