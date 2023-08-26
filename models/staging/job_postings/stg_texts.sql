with job_postings as (
    select * from {{ source('raw_jobs', 'job_postings')}}
),

stg_texts as (

    select
        id,
        text,
        translate(text, chr(160), ' ') as with_breaking_spaces,
        trim(with_breaking_spaces, '\n ') as trimmed,
        replace(trimmed, '\n', ' ') as cleaned_text     
    from job_postings
)

select id, text, cleaned_text from stg_texts
