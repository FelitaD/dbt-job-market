with unpivoted as (
    select * from {{ ref('stg_unpivoted_extraction') }}
),

extracted_keywords as (
    select 
        {{ dbt_utils.generate_surrogate_key(['id', 'key']) }}
            as job_keyword_id,
        id,
        key,
        value
    from unpivoted
    where value like 'true'
)

select * from extracted_keywords order by id