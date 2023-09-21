all_companies_stmt = """
    select *
    from `job_market.companies`; 
"""

relevant_jobs_stmt = """
    select 
        title,
        company,
        rating, 
        reviews,
        size,
        remote,
        location,
        stack,
        text,
        j.url as job_url,
        c.url as company_url,
        contract,
        created_at,
        id,
        apply,
        applied
    from `job_market.jobs` j
    left join `job_market.companies` c
    on lower(j.company) = lower(c.company_name)
    where regexp_contains(title, r'(?i).*(data|analytics).*(engineer|ingénieur).*|.*(engineer|ingénieur).*(data|données|big data|bigdata)')
    order by rating desc, reviews desc, created_at desc;
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