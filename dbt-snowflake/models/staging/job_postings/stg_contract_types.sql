with job_postings as (
    select * from {{ source('raw_jobs', 'job_postings')}}
),

stg_contract_types as (

    select
        id,
        contract,
        case 
            when contract like '%CDI%' or contract like '%Permanent%' then 'Full Time'
            when contract like '%Alternance%' or contract like '%Stage%' or contract like '%Internships%' then 'Graduate program'
            when contract like '%VIE%' or contract like '%CDD / Temporaire%' or contract like '%Autres%' then 'Other'
            when contract like 'N' then NULL
            else contract
        end as simplified_contract
    from job_postings
)

select * from stg_contract_types
