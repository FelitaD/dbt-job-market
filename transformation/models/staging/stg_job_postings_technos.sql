{{ config(materialized='table') }}

with unpivoted_numbered as (
    select job_id, keyword, text from {{ ref('stg_unpivoted_numbered') }}
),

job_postings as (
    select id, url, title, company, location, contract, industry, remote, created_at from {{ ref('stg_job_postings') }}
),

technos as (
    select name as techno, keyword
    from {{ ref('technos') }}
),

join_job_postings as (
    select  
        *,
        lower(replace(u.keyword, '_', ' ')) as keyword
    from unpivoted_numbered u
    join job_postings j
    on u.job_id = j.id
),

job_postings_technos as (
    select *
    from join_job_postings j
    join technos t
    using(keyword)
)

select id, title, company, techno,
        location, remote, contract, industry, text, url, created_at
from job_postings_technos