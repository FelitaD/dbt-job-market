{{ config(materialized='table') }}

with unpivoted as ( {{ 
    dbt_utils.unpivot(
      ref('stg_pivoted_extraction'),
      cast_to='variant',
      field_name='keyword',
      value_name='details',
      exclude=[
        'job_id',
        'url',
        'title',
        'company',
        'sentence_text'
      ],
      remove = []
    ) 
  }} )
  
select * from unpivoted
