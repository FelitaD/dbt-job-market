with job_postings as (
    select * from {{ source('raw_jobs', 'job_postings')}}
),

stg_texts as (

    select
        id,
        text,
        trim(text, '\n ') as trimmed,
        replace(trimmed, '\n', ' ') as cleaned_text     
    from job_postings
)

select * from stg_texts
