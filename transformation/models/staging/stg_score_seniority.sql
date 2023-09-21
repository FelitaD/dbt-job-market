-- junior : 3
-- data engineer : 1
-- intern data engineer : 0
-- senior : -1

with jobs as (
    select * from {{ ref('jobs') }}
),

seniority  as (
    select
        id,
        case 
            when contract like 'Graduate program' then 0
            when regexp_contains(title, r'(?i)junior') then 3
            when regexp_contains(title, r'(?i)senior|lead|confirmed|confirmé|expérimenté') then -1
            else 1
        end as seniority_score
    from jobs
)

select id, seniority_score from seniority