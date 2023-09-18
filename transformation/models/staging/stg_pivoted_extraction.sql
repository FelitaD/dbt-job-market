{% set sql_statement %}
    select 
        keyword, 
        keyword_regex, 
        keyword_category 
    from {{ ref('stg_base_keywords') }}
{% endset %}

{%- set query_results = dbt_utils.get_query_results_as_dict(sql_statement) -%}

with jobs as (
  select * from {{ ref("stg_job_postings") }}
),

mentions as (
    select
        id as job_id,
        text,
        {%- for k in query_results['KEYWORD'] | list %}
        {%- set regex = query_results['KEYWORD_REGEX'][loop.index-1] %}
        regexp_like(text, $$.*[\s,.\n]({{ regex }})[\s,.\n].*$$, 'i')
            as {{ k | replace(" ","_") | replace("|","_") | lower }} {{ "," if not loop.last}}
       {%- endfor %}

    from jobs
)

select * from mentions