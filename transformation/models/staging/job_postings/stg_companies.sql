with job_postings as (
    select * from {{ source('raw_jobs', 'job_postings')}}
),

companies  as (
    select 
        id,
        initcap(company) as company
    from job_postings
)

select * from companies