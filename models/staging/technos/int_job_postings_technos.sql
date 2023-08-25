{{ config(materialized='table') }}

with unpivoted_numbered as (
    select * from {{ ref('stg_unpivoted_numbered') }}
),

job_postings as (
    select * from {{ ref('int_job_postings') }}
),

job_postings_technos as (
    select  j.id,
            j.url,
            j.title,
            j.company,
            initcap(replace(u.keyword, '_', ' ')) as techno,
            initcap(u.keyword_category) as techno_category,
            j.location,
            j.remote,
            j.contract,
            j.industry,
            u.sentence_text,
            j.text
    from unpivoted_numbered u
    join job_postings j
    on u.job_id = j.id
)

select * from job_postings_technos