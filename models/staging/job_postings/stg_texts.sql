with job_postings as (
    select * from {{ source('raw_jobs', 'job_postings')}}
),

stg_texts as (

    select
        id,
        text,
        REGEXP_REPLACE(
            text,
            '(\r?\n)+',
            '\n', 
            1, 0, 'm'
        ) as cleaned_text
    from job_postings
)

select * from stg_texts
