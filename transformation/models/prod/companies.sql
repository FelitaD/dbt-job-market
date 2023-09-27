with stg_companies as (
    select * from {{ source('companies', 'stg_companies') }}
),

intermediate_companies as (
    select
        company_name,  
        details, 
        reviews,
        case 
            when url like 'None' then NULL
            else url
        end as url,
        case 
            when rating like 'None' then NULL
            else regexp_extract(rating, r'\d\.\d') 
        end as rating,
        case
            when name like 'None' then NULL
            else name
        end as name, 
        case
            when details like 'None' then NULL
            else regexp_extract(details, r'[\d]+K?.*[\d]*K?')
        end as int_size,
        case
            when details like 'None' then NULL
            else regexp_extract(details, r'(?i)^[A-Z\s&,]+')
        end as industry,
        case 
            when headquarters like 'None' then NULL
            else headquarters
        end as headquarters,
        case
            when jobs like 'None' then NULL
            else jobs
        end as int_jobs,
        case
            when salaries like 'None' then NULL
            else salaries
        end as int_salaries,
    from stg_companies
),

companies as (
    select 
        company_name,
        name,
        url, 
        rating,
        case 
            when industry is not null then regexp_replace(industry, r'\\n', '')
        end as industry,
        case
            when headquarters is not null then regexp_replace(headquarters, r'(Headquarters.near.)', '')
            else headquarters
        end as headquarters,
        case 
            when regexp_contains(int_size, r'(1 to 50).Employees') then 25
            when regexp_contains(int_size, r'(51 to 200).Employees') then 125
            when regexp_contains(int_size, r'(201 to 500).Employees') then 350
            when regexp_contains(int_size, r'(501 to 1K).Employees') then 750
            when regexp_contains(int_size, r'(1K to 5K).Employees') then 3000
            when regexp_contains(int_size, r'(5K to 10K).Employees') then 7500
            when regexp_contains(int_size, r'(10K\+).Employees') then 15000
        end as company_size,
        case 
            when regexp_contains(reviews, 'K') then regexp_replace(reviews, 'K', '000') 
            else reviews
        end as reviews_count,
        case 
            when regexp_contains(int_jobs, 'K') then regexp_replace(int_jobs, 'K', '000')
            else int_jobs
        end as jobs_count,
        case 
            when regexp_contains(int_salaries, 'K') then regexp_replace(int_salaries, 'K', '000')
            else int_salaries
        end as salaries_count,
    from intermediate_companies
)

select 
    company_name,
    name,
    url, 
    industry,
    headquarters,
    safe_cast(rating as numeric) as rating,
    safe_cast(company_size as integer) as company_size,
    safe_cast(reviews_count as integer) as reviews_count,
    safe_cast(jobs_count as integer) as jobs_count,
    safe_cast(salaries_count as integer) as salaries_count
from companies