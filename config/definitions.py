import os
from pathlib import Path

PROJECT_PATH = Path(__file__).parent.parent.resolve()

JOB_MARKET_DB_PWD = os.environ['JOB_MARKET_DB_PWD']
JOB_MARKET_DB_USER = os.environ['JOB_MARKET_DB_USER']
DB_STRING = f"postgresql://{JOB_MARKET_DB_USER}:{JOB_MARKET_DB_PWD}@localhost:5432/job_market"
SNOWSQL_PWD = os.getenv('SNOWSQL_PWD')
WAREHOUSE = os.getenv('WAREHOUSE')
SNOWFLAKE_ACCOUNT = os.getenv('SNOWFLAKE_ACCOUNT')
SNOWFLAKE_ROLE = os.getenv('SNOWFLAKE_ROLE')
SNOWFLAKE_USER = os.getenv('SNOWFLAKE_USER')
OCTOPARSE_USER = os.getenv('OCTOPARSE_USER')
OCTOPARSE_PWD = os.getenv('OCTOPARSE_PWD')

all_data_columns = ['company_name', 'name', 'url', 'industry', 'headquarters', 'rating',
                    'company_size', 'reviews_count', 'jobs_count', 'salaries_count', 'id',
                    'company', 'contract', 'created_at', 'industry_1', 'location', 'remote',
                    'stack', 'text', 'title', 'url_1', 'id_1', 'is_relevant',
                    'is_same_glassdoor', 'seniority_score', 'rating_score', 'total_score']

# Google SQL queries

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