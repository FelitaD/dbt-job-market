-- Check if scores are behaving in expected way

with jobs as (
    select * from {{ ref('jobs') }}
),

scores as (
    select * from {{ ref('scores') }}
),

companies as (
    select * from {{ ref('companies') }}
)

select 
    id,
    title,
    contract,
    is_relevant_score,
    seniority_score,
    company,
    name, 
    is_same_glassdoor_score,
    rating,
    rating_score
from jobs
join scores using(id)
join companies on companies.company_name = jobs.company