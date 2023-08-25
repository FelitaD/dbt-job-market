{{ config(materialized='table') }}

with unpivoted as (
    select * from {{ ref('stg_unpivoted_extraction') }}
),

extracted_keywords as (
    select 

    {{ dbt_utils.generate_surrogate_key(['job_id', 'sentence_text', 'keyword']) }}
        as keyword_sentence_id,
    job_id,
    url,
    title,
    company,
    keyword,
    details:category :: text as keyword_category,
    sentence_text,
    details:substring :: text as match_substring
    from unpivoted
    where match_substring is not null
)

select * from extracted_keywords