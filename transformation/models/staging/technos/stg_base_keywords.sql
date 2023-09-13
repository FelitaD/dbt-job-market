with source as (
    select * from {{ ref('base_keywords') }}
),

renamed as (
  select
    name :: text as name,
    keyword :: text as keyword,
    additional_regex :: text as additional_regex,
    case when additional_regex is not null
      then keyword || '|' || additional_regex
      else keyword
    end as keyword_regex,
    category :: text as keyword_category,
    subcategory :: text as keyword_subcategory,
    location :: text as location,
    year :: number as founding_year,
    website :: text as website, 
    summary :: text as summary

  from
    source
),

renamed_numbered as (
    select 
        *, 
        row_number() over(partition by keyword order by keyword) as rn 
    from renamed)


select * from renamed_numbered where rn = 1