with source as (
    select * from {{ source('raw_jobs', 'job_postings')}}
),

job_postings as (

    select 
        source.id as id,
        urls.cleaned_url as url,
        titles.trimmed as title,
        source.company as company,
        source.location as location,
        contracts.simplified_contract as contract,
        source.industry as industry,
        remote_policies.simplified_remote as remote,
        texts.cleaned_text as text

    from source
    join {{ ref('stg_urls') }} as urls on source.id = urls.id
    join {{ ref('stg_titles') }} as titles on source.id = titles.id
    join {{ ref('stg_contract_types') }} as contracts on source.id = contracts.id
    join {{ ref('stg_remote_policies' )}} as remote_policies on source.id = remote_policies.id
    join {{ ref('stg_texts') }} as texts on source.id = texts.id
)

select * from job_postings
