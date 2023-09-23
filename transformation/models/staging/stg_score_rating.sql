-- below 20% : -3
-- between 20% and 40% : -2
-- between 40% and 50% : -1
-- equal to 50% : 0
-- between 50% and 60% : 1
-- between 60% and 80% : 2
-- above 80% : 3

with companies as (
    select * from {{ ref('companies') }}
),

jobs as (
    select id, company from {{ ref('jobs') }}
),

percentiles as (
    select
        percentile_cont(rating, 0) over() as min,
        percentile_cont(rating, 0.2) over() as percentile20,
        percentile_cont(rating, 0.4) over() as percentile40,
        percentile_cont(rating, 0.5) over() as median,
        percentile_cont(rating, 0.6) over() as percentile60,
        percentile_cont(rating, 0.8) over() as percentile80,
        percentile_cont(rating, 1) over() as max
    from companies limit 1
),

score as (
    select
        id,
        rating,
        case 
            when rating between min and percentile20 then -3
            when rating between percentile20 and percentile40 then -2
            when percentile40 < rating and rating < median then -1
            when rating = median  then 0
            when median < rating and rating < percentile60 then 1
            when rating between percentile60 and percentile80 then 2
            when rating > percentile80 then 3
        end as rating_score
    from percentiles, companies c
    join jobs j
    on c.company_name = j.company
)

select id, rating_score from score
