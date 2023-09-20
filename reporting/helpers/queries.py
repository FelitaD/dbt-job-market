all_jobs_companies_stmt = """
    select 
        title,
        company,
        stack,
        *
    from `job_market.jobs` j
    join `job_market.companies` c
    on j.company = c.company_name
    order by rating desc, reviews desc, created_at desc;
"""

relevant_jobs_stmt = """
    select 
        apply,
        title,
        company,
        stack,
        rating, 
        reviews,
        size,
        remote,
        text,
        j.url as job_url,
        c.url as company_url,
        created_at,
    from `job_market.jobs` j
    join `job_market.companies` c
    on j.company = c.company_name
    where regexp_contains(title, r'(?i).*(data|analytics).*(engineer|ingénieur).*|.*(engineer|ingénieur).*(data|données|big data|bigdata)')
    and title not like 'Senior%'
    and contract not like 'Graduate program'
    and remote not like 'ponctual'
    order by rating desc, reviews desc, created_at desc;
"""

techno_occurences_stmt = """
select distinct name, total, category, subcategory, description
    from (
        select count(*) as total, name from job_market.technos group by name
        ) as techno_count t
    join job_market.stg_job_postings_technos j
    on t.keyword = j.techno
    order by total desc
"""