companies_stmt = """
    select *
    from `job_market.companies`; 
"""

all_data_stmt = """
    select * 
    from `job_market.companies` c
    join `job_market.jobs` j 
    on c.company_name = j.company
    join `job_market.scores` s
    on j.id = s.id
    where is_relevant = 1
    order by total_score desc, created_at desc;
"""

technos_stmt = """
select distinct techno, total, category, subcategory, description
from (
    select count(*) as total, techno from `job_market.stg_job_postings_technos` group by techno
    ) as j
join `job_market.technos` t
on t.name = j.techno
order by total desc;
"""

sankey_stmt = """
select * from `job_market.sankey_data`;
"""