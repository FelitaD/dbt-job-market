{%- set query_results = dbt_utils.get_query_results_as_dict('select keyword, keyword_regex, keyword_category from ' ~ ref('stg_base_keywords')) -%}

with base_flatten_sentences as(
    select * from {{ ref('stg_base_sentences_flatten') }}
),

mentions as (
    select
        sentence_id,
        job_id,
        url,
        title,
        company,
        sentence_text,
        {%- for k in query_results['KEYWORD'] | list %}
        {%- set regex = query_results['KEYWORD_REGEX'][loop.index-1] %}
        {%- set category = query_results['KEYWORD_CATEGORY'][loop.index-1] %}
        object_construct_keep_null(
            'substring', regexp_substr( sentence_text, '{{ regex }}', 1, 1, 'i'),
            'category', '{{category}}'
        ) as {{ k | replace(" ","_") | replace("|","_") | lower }} {{ "," if not loop.last}}
       {%- endfor %}

    from base_flatten_sentences
)

select * from mentions