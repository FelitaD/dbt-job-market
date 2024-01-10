{%- set HF = 'H\s?\/?\s?F' %}
{%- set FH = 'F\s?\/?\s?H' %}
{%- set HFX = 'H\s?\/?\s?F\s?\/?\s?X' %}
{%- set MFD = 'M\s?\/?\s?F\s?\/?\s?D' %}
{%- set FMD = 'F\s?\/?\s?M\s?\/?\s?D' %}
{%- set MWD = 'M\s?\/?\s?W\s?\/?\s?D' %}
{%- set MW = 'M\s?\/?\s?W' %}
{%- set HST = 'H\s?\/?\s?S\s?\/?\s?T' %}

with raw_job_postings as (
    select * from {{ source('raw_job_postings', 'raw_job_postings')}}
),

stg_job_postings as (

    select 

        -- company
        initcap(company) as clean_company,

        -- contract
        case 
            when contract like '%CDI%' or contract like '%Permanent%' then 'Full Time'
            when contract like '%Alternance%' or contract like '%Stage%' or contract like '%Internships%' then 'Graduate program'
            when contract like '%VIE%' or contract like '%CDD / Temporaire%' or contract like '%Autres%' or contract like '%Temps partiel%' then 'Other'
            when contract like 'N' then NULL
            else contract
        end as clean_contract,

        -- created_at
        created_at,

        -- industry
        industry,

        -- location
        location, 

        -- remote    
        case 
            when remote like '%total%' then 'total'
            when remote like '%partiel%' or remote like '%régulier%' or remote like '%fréquent%' then 'partial'
            when remote like '%occasionnel%' or remote like '%ponctuel%' then 'ponctual'
            when (remote like 'N' or remote IS NULL) and url like '%linkedin%' then 'total'
            when remote like 'N' or remote like '%Télétravail non autorisé%' then NULL
            else remote
        end as clean_remote,

        -- text 
        replace(trim(translate(text, chr(160), ' '), '\n '), '\n', ' ') as clean_text,

        -- title
        trim(regexp_replace(regexp_replace(title, r'(?i)[(].*[)]', ''), r'(?i){{ HF }}|{{ FH }}|{{ HFX }}|{{ MFD }}|{{ FMD }}|{{ MWD }}|{{ MW }}|{{ HST }}', '')) as clean_title,
        
        -- url
        case 
            when url like '%?q=%' then split(url, '?q=')[OFFSET(0)] 
            else url 
        end as clean_url,

    from raw_job_postings
)

select 
    row_number() over() as id, 
    clean_company as company, 
    clean_contract as contract, 
    created_at, 
    industry,
    location,
    clean_remote as remote,
    clean_text as text,
    clean_title as title,
    clean_url as url
from stg_job_postings
