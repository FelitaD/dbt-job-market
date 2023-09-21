all_companies_stmt = """
    select *
    from `job_market.companies`; 
"""

all_data_stmt = """
    select * 
    from `job_market.companies` c
    join `job_market.jobs` j 
    on c.company_name = j.company
    join `job_market.scores` s
    on j.id = s.id; 
"""

relevant_jobs_stmt = """
    select 
        total_score,
        is_relevant_score,
        seniority_score,
        rating_score,
        is_same_glassdoor_score,
        title,
        company,
        j.url as job_url,
        c.url as company_url,
        rating, 
        reviews,
        stack,
        remote,
        location,
        created_at,
        text,
        apply,
        applied,
        id,
    from `job_market.jobs` j
    left join `job_market.companies` c
    on j.company = c.company_name
    join `job_market.scores` s
    using(id)
    order by total_score desc;
"""

techno_occurences_stmt = """
select distinct techno, total, category, subcategory, description
from (
    select count(*) as total, techno from job_market.stg_job_postings_technos group by techno
    ) as j
join job_market.technos t
on t.name = j.techno
order by total desc;
"""