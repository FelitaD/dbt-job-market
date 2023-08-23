with source as (
    select * from {{ source('raw_jobs', 'job_postings')}}
),

truncated_urls as (

    select
        case
            when url like '%?q=%' then split_part(url, '?q=', 1)
            else url
        end as cleaned_url

    from source
)

select * from truncated_urls