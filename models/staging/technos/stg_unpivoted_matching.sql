{{ config(materialized='table') }}

with unpivoted as (
    select * from {{ ref('stg_unpivoted_extraction') }}
),

extracted_keywords as (
    select 
        {{ dbt_utils.generate_surrogate_key(['job_id', 'text', 'keyword']) }}
            as keyword_text_id,
        job_id,
        keyword,
        text,
        is_present
    from unpivoted
    where is_present like 'true'
)

select * from extracted_keywords