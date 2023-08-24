{%- set query_results = dbt_utils.get_query_results_as_dict('select keyword, keyword_regex, keyword_category from ' ~ ref('base_keywords')) -%}

with base_posts as(
    select * from {{ ref('base_post_sentences') }}
),

mentions as (
    select
        sentence_id,
        post_id,
        author,
        url,
        title,
        sentence_text,

        {% for k in query_results['KEYWORD'] | list %}
        {%- set regex = query_results['KEYWORD_REGEX'][loop.index-1] %}
        {%- set category = query_results['KEYWORD_CATEGORY'][loop.index-1] %}
        object_construct_keep_null(
            'substring', regexp_substr( sentence_text, '{{ regex }}', 1, 1, 'i'),
            'category', '{{category}}',
            'start_position', regexp_instr( sentence_text, '{{ regex }}', 1, 1, 0, 'i'),
            'end_position', regexp_instr( sentence_text, '{{ regex }}', 1, 1, 1, 'i')
        ) as {{ k | replace(" ","_") | replace("|","_") | lower }} {{ "," if not loop.last}}
       {%- endfor %}

    from base_posts
)

select * from mentions