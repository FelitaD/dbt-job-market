with sentences as (
  select * from {{ ref("stg_base_sentences") }}
),

flatten as (
    select 
        id as job_id,
        url,
        title,
        company,
        s.value :: text as sentence_text,
        {{ dbt_utils.generate_surrogate_key(['job_id', 'index', 'sentence_text']) }} as sentence_id
    from sentences,
        lateral flatten(input => sentence_text_list) as s
)

select * from flatten