with job_postings as (
    select * from {{ source('raw_jobs', 'job_postings')}}
),

stg_remote_policies as (

    select
        id,
        remote,
        case 
            when remote like '%total%' then 'total'
            when remote like '%partiel%' or remote like '%régulier%' then 'partial'
            when remote like '%occasionnel%' or remote like '%ponctuel%' then 'ponctual'
            when remote like 'N' then NULL
            else remote
        end as simplified_remote
    from job_postings
)

select * from stg_remote_policies
