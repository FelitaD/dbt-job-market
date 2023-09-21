-- Evaluate if companies Glassdoor name is the same or if investigation must be made (to avoid wrong rating).

-- Name exactly the same: 1
-- Name different: 0
-- Not found: -1

with companies as (
    select * from {{ source('companies', 'companies') }}
),

jobs as (
    select id, company from {{ ref('jobs') }}
),

score as (
    select 
        id,
        case 
            when lower(name) not like lower(company) then 0
            when lower(name) like lower(company) then 1
            when name like 'None' then -1
        end as is_same_glassdoor_score
    from companies c
    join jobs j
    on c.company_name = j.company
)

select id, is_same_glassdoor_score from score