with keywords as ( select * from {{ref('base_keywords')}} )

select array_agg(keyword_regex) from keywords

