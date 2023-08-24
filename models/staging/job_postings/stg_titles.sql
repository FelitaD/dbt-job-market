{%- set HF = 'H\s?\/?\s?F' %}
{%- set FH = 'F\s?\/?\s?H' %}
{%- set HFX = 'H\s?\/?\s?F\s?\/?\s?X' %}
{%- set MFD = 'M\s?\/?\s?F\s?\/?\s?D' %}
{%- set FMD = 'F\s?\/?\s?M\s?\/?\s?D' %}
{%- set MWD = 'M\s?\/?\s?W\s?\/?\s?D' %}
{%- set MW = 'M\s?\/?\s?W' %}
{%- set HST = 'H\s?\/?\s?S\s?\/?\s?T' %}

with job_postings as (
    select * from {{ source('raw_jobs', 'job_postings')}}
),

stg_titles as (

    select
        id,
        title,
        REGEXP_REPLACE(
            title,
            '[(].*[)]',
            '', 
            1, 0, 'im'
            ) as minus_parenthesis,
        REGEXP_REPLACE(
            minus_parenthesis,
            '{{ HF }}|{{ FH }}|{{ HFX }}|{{ MFD }}|{{ FMD }}|{{ MWD }}|{{ MW }}|{{ HST }}',
            '', 
            1, 0, 'im'
            ) as minus_gender
    from job_postings
)

select * from stg_titles
