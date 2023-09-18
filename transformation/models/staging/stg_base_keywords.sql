with base_keywords as (
    select * from {{ ref('base_keywords') }}
),

renamed as (
  select
    -- additional regex
    additional_regex :: text as additional_regex,

    -- category
    category :: text as keyword_category,

    -- founding_year
    year :: number as founding_year,

    -- keyword
    keyword :: text as keyword,

    -- keyword_regex
    case when additional_regex is not null
      then keyword || '|' || additional_regex
      else keyword
    end as keyword_regex,

    -- location
    location :: text as location,

    -- name
    name :: text as name,

    -- subcategory
    subcategory :: text as keyword_subcategory,

    -- summary
    summary :: text as summary

    -- website
    website :: text as website, 

  from
    base_keywords
),

renamed_numbered as (
    select 
        *, 
        row_number() over(partition by keyword order by keyword) as rn 
    from renamed
)


select * from renamed_numbered where rn = 1