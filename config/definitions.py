import os
from pathlib import Path

PROJECT_PATH = Path(__file__).parent.parent.resolve()

all_data_columns = ['company_name', 'name', 'url', 'industry', 'headquarters', 'rating',
                    'company_size', 'reviews_count', 'jobs_count', 'salaries_count', 'id',
                    'company', 'contract', 'created_at', 'industry_1', 'location', 'remote',
                    'stack', 'text', 'title', 'url_1', 'id_1', 'is_relevant',
                    'is_same_glassdoor', 'seniority_score', 'rating_score', 'total_score']

# GoogleSQL queries

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

companies_stmt = """
    select *
    from `job_market.companies`; 
"""

sankey_stmt = """
select * from `job_market.sankey_data`;
"""

all_jobs_stmt = """
    select * 
    from `job_market.companies` c
    join `job_market.jobs` j 
    on c.company_name = j.company
    join `job_market.scores` s
    on j.id = s.id
    order by total_score desc, created_at desc;
"""