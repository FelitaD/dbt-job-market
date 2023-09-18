{{ config(materialized='table') }}

with job_postings_technos as (
    select * from {{ ref('stg_job_postings_technos') }}
),

jobs as (
    select 
        id,
        title, 
        company,
        listagg(techno, ', ') as stack,
        location,
        remote, 
        industry, 
        contract, 
        url, 
        text, 
        created_at
    from job_postings_technos
    group by id, title, company, location, remote, industry, contract, url, text, created_at
)

select * from jobs