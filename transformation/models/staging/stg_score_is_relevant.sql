-- Evaluate the relevance of the position based on the `title` and `contract` of the job.

-- data/anlaytics engineer : 1
-- non data engineer : 0

with jobs as (
    select * from {{ ref('jobs') }}
),

relevance as (
    select
        id, 
        title,
        contract,
        case 
            when regexp_contains(title, r'(?i).*(data|analytics).*(engineer|ingénieur).*|.*(engineer|ingénieur).*(data|données|big data|bigdata)') then 1
            else 0
        end as is_relevant
    from jobs
)

select id, is_relevant from relevance