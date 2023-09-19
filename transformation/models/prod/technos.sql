with base_keywords as (
    select * from {{ source('base_keywords', 'base_keywords') }}
    where category not like 'Applications%'
),

renamed as (
  select
    -- additional regex
    additional_regex,

    -- category
    category,

    -- description
    summary as description,

    -- founding_year
    founding_year,

    -- keyword
    keyword,

    -- keyword_regex
    case when additional_regex is not null
      then keyword || '|' || additional_regex
      else keyword
    end as keyword_regex,

    -- location
    location,

    -- name
    name,

    -- subcategory
    subcategory,

    -- website
    website, 

  from
    base_keywords
),

renamed_numbered as (
    select 
        *, 
        row_number() over(partition by keyword order by keyword) as rn 
    from renamed
)

select 
    additional_regex,  
    category,
    description,
    founding_year,
    keyword,
    keyword_regex,
    location,
    name,
    subcategory,
    website
from renamed_numbered where rn = 1