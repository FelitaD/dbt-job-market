with source as (
  select * from {{ ref('keywords') }}
),

renamed as (
  select

    -- keys
    keyword :: text as keyword,

    -- details
    additional_regex :: text as additional_regex,
    category :: text as keyword_category,
    case when additional_regex is not null
      then keyword || '|' || additional_regex
      else keyword
    end as keyword_regex

  from
    source
)

select * from renamed