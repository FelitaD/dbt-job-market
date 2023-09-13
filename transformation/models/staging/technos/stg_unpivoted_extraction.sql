with unpivoted as ( {{ 
    dbt_utils.unpivot(
      ref('stg_pivoted_extraction'),
      cast_to='boolean',
      field_name='keyword',
      value_name='is_present',
      exclude=[
        'job_id',
        'text'
      ],
      remove = []
    ) 
  }} )
  
select * from unpivoted
