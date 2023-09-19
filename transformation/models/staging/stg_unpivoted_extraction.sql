{{ config(
  pre_hook = "{{ create_f_fhoffa_x_unpivot() }}"
) }}

with pivoted as ((
    select * from {{ ref('stg_pivoted_extraction') }}
))
  
select 
    id, 
    unpivoted.key, 
    unpivoted.value 
from pivoted p, unnest(job_market.fhoffa_x_unpivot(p, 'k_')) unpivoted

