{{ config(materialized='table') }}

with job_postings_technos as (
    select * from {{ ref('stg_job_postings_technos') }}
),

jobs as (
    select 
        id,
        company,
        contract, 
        created_at,
        industry, 
        location,
        remote, 
        array_agg(techno order by techno) as stack,
        text, 
        title, 
        url, 
    from job_postings_technos
    group by id, company, contract, created_at, industry, location, remote, text, title, url
)

select * from jobs order by created_at desc, id