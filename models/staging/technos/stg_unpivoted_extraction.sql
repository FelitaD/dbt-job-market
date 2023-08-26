with unpivoted as ( {{ 
    dbt_utils.unpivot(
      ref('stg_pivoted_extraction'),
      cast_to='boolean',
      field_name='keyword',
      value_name='details',
      exclude=[
        'job_id',
        'sentence_id',
        'sentence_text'
      ],
      remove = []
    ) 
  }} )
  
select * from unpivoted
