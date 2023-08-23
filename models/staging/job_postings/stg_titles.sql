{%- set HF = 'H\s?\/?\s?F' %}
{%- set FH = 'F\s?\/?\s?H' %}
{%- set HFX = 'H\s?\/?\s?F\s?\/?\s?X' %}
{%- set MFD = 'M\s?\/?\s?F\s?\/?\s?D' %}
{%- set FMD = 'F\s?\/?\s?M\s?\/?\s?D' %}
{%- set MWD = 'M\s?\/?\s?W\s?\/?\s?D' %}
{%- set MW = 'M\s?\/?\s?W' %}
{%- set HST = 'H\s?\/?\s?S\s?\/?\s?T' %}

with source as (
    select * from {{ source('raw_jobs', 'job_postings')}}
),

stg_titles  as (

    select
        id,
        title,
        REGEXP_REPLACE(
            title,
            '{{ HF }}|{{ FH }}|{{ HFX }}|{{ MFD }}|{{ FMD }}|{{ MWD }}|{{ MW }}|{{ HST }}',
            '', 
            1, 0, 'im'
            ) as without_gender,
        REGEXP_REPLACE(
            without_gender,
            '[()]',
            '', 
            1, 0, 'im'
            ) as without_empty_parenthesis
    from source
)

select without_empty_parenthesis as title from stg_titles
