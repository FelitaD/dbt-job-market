## Steps to modify Job Radar 1.0 Transformation

- [x] Set up Snowflake connection

**Preprocessing url, title, remote, contract, text**
- [x] Add raw_jobs.job_postings source + tests + doc
- [x] Add job_postings config file + tests + doc
- [x] Add stg_urls model + tests + doc
- [x] Add stg_titles model + tests + doc
- [x] Add stg_remote_policies model + tests + doc
- [x] Add stg_types model + tests + doc
- [x] Add stg_texts model + tests + doc
- [x] Add job_postings model + tests + doc

**Processing text: extract technos**
- [ ] Add seed with technos csv
- [ ] Use regex_substr_all to get technos in new column as an array