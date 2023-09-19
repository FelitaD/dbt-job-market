with unpivoted_numbered as (
    select 
        id, 
        regexp_replace(regexp_replace(key, r'^(k_)', ''), r'_', ' ') as keyword
    from {{ ref('stg_unpivoted_numbered') }}
),

job_postings as (
    select 
        id, 
        company, 
        contract, 
        created_at,
        industry, 
        location, 
        title, 
        remote, 
        text, 
        url, 
    from {{ ref('stg_job_postings') }}
),

technos as (
    select 
        keyword,
        name as techno
    from {{ ref('technos') }}
),

job_postings_technos as (
    select 
        id, 
        company,
        contract,
        created_at,
        industry,
        location,
        remote, 
        techno,
        text,
        title, 
        url,
    from unpivoted_numbered u
    join job_postings j
    using(id)
    join technos t
    using(keyword)
)

select * from job_postings_technos
