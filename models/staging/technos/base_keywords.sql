with source as (
  select * from {{ ref('keywords') }}
),

renamed as (
  select
    name :: text as name,
    keyword :: text as keyword,
    additional_regex :: text as additional_regex,
    category :: text as keyword_category,
    subcategory :: text as keyword_subcategory,
    location :: text as location,
    year :: number as founding_year,
    funding :: text as funding,
    website :: text as website, 
    summary :: text as summary,
    case when additional_regex is not null
      then keyword || '|' || additional_regex
      else keyword
    end as keyword_regex

  from
    source
)

select * from renamed