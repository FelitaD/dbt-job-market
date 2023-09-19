{% set sql_statement %}
    select 
        keyword, 
        keyword_regex
    from {{ ref('technos') }}
{% endset %}

{%- set query_results = dbt_utils.get_query_results_as_dict(sql_statement) -%}


with jobs as (
  select * from {{ ref("stg_job_postings") }}
),

mentions as (
    select
        id,
        {%- for k in query_results['keyword'] | list %}
        {%- set regex = query_results['keyword_regex'][loop.index-1] %}
        regexp_contains(text, r'(?i).*[\s,.\n]({{ regex }})[\s,.\n].*')
            as `{{ 'k_' + k | replace(" ","_") | replace("|","_") | lower }}` {{ "," if not loop.last}}
       {%- endfor %}

    from jobs
)

select * from mentions