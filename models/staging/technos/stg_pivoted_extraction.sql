{% set sql_statement %}
    select 
        keyword, 
        keyword_regex, 
        keyword_category 
    from {{ ref('stg_base_keywords') }}
{% endset %}

{%- set query_results = dbt_utils.get_query_results_as_dict(sql_statement) -%}

with base_sentences_flatten as(
    select * from {{ ref('stg_base_sentences_flatten') }}
),

mentions as (
    select
        sentence_id,
        job_id,
        sentence_text,
        {%- for k in query_results['KEYWORD'] | list %}
        {%- set regex = query_results['KEYWORD_REGEX'][loop.index-1] %}
        regexp_like(sentence_text, '.*({{ regex }}).*')
            as {{ k | replace(" ","_") | replace("|","_") | lower }} {{ "," if not loop.last}}
       {%- endfor %}

    from base_sentences_flatten
)

select * from mentions