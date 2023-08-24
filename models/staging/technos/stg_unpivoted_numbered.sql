with unpivoted_matching as (
    select * from {{ ref('stg_unpivoted_matching') }}
),

numbered_job_id_keyword as (

    select *,
           row_number() over(partition by job_id, keyword order by keyword_sentence_id) as rn
    FROM unpivoted_matching
)

select * from numbered_job_id_keyword where rn = 1 order by job_id