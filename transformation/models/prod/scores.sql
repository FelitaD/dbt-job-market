with jobs as (
    select * from {{ ref('jobs') }}
),

scores as (
    select
        jobs.id as id, 

        is_relevant,
        -- data/analytics engineer : 1
        -- non data engineer : 0

        is_same_glassdoor,
        -- name exactly the same: 1
        -- name different: 0
        -- not found: -1

        seniority_score,
        -- junior : 3
        -- data engineer : 1
        -- intern data engineer : 0
        -- senior : -1
        
        rating_score, 
        -- below 20% : -3
        -- between 20% and 40% : -2
        -- between 40% and 50% : -1
        -- equal to 50% : 0
        -- between 50% and 60% : 1
        -- between 60% and 80% : 2
        -- above 80% : 3

        seniority_score + rating_score as total_score

    from jobs
    join {{ref('stg_score_is_relevant')}} a on a.id = jobs.id
    join {{ref('stg_score_glassdoor_is_same')}} b on b.id = jobs.id
    join {{ref('stg_score_rating')}} c on c.id = jobs.id
    join {{ref('stg_score_seniority')}} d on d.id = jobs.id
)

select * from scores order by total_score desc