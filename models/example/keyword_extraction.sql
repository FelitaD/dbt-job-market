with unpivoted as (
  {{ 
    dbt_utils.unpivot(
      ref('stg_keyword_extraction'),
      cast_to='variant',
      field_name='keyword',
      value_name='details',
      exclude=[
        'post_id',
        'author',
        'url',
        'title',
        'sentence_text'
      ],
      remove = []
    ) 
  }}
)
select

  {{ dbt_utils.surrogate_key(['post_id', 'sentence_text', 'keyword']) }}
    as keyword_sentence_id,
  post_id,
  author,
  url,
  title,
  keyword,
  details:category :: text as keyword_category,
  sentence_text,
  details:substring :: text as match_substring,
  details:start_position :: integer as start_position,
  details:end_position  :: integer as end_position

from unpivoted
where match_substring is not null