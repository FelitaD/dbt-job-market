-- junior : 1
-- data engineer : 0
-- intern data engineer : -1
-- senior : -2

with jobs as (
    select * from {{ ref('jobs') }}
),

seniority  as (
    select
        id,
        case 
            when contract like 'Graduate program' then -1
            when regexp_contains(title, r'(?i)junior') then 1
            when regexp_contains(title, r'(?i)senior|lead|confirmed|confirmé|expérimenté') then -2
            else 0
        end as seniority_score
    from jobs
)

select id, seniority_score from seniority