from datetime import datetime

import pandas as pd
from sqlalchemy.engine import create_engine
from sqlalchemy import text
from google.cloud import bigquery

from config.definitions import PROJECT_PATH


def fetch_companies():
    """

    """
    custom_bq_client = bigquery.Client()

    engine = create_engine(
        'bigquery://resume-404711/job-market?user_supplied_client=True',
        connect_args={'client': custom_bq_client},
    )
    with engine.connect() as connection:
        # We only want companies from listings that aren't already present in the companies table
        stmt = text(
            """
            select distinct(company) 
            from job_market.jobs as j
            where not exists (
                select * from job_market.companies as c
                where j.company = c.company_name
            );
            """
        )
        data = connection.execute(stmt).fetchall()

    return [t[0] for t in data]


def generate_urls(companies):
    formatted_companies = [company.split('|')[0] for company in companies]
    formatted_companies = [company.replace(' ', '%20') for company in formatted_companies]
    base_url = 'https://www.glassdoor.com/Search/results.htm?keyword={}'
    return [base_url.format(company) for company in formatted_companies]


def save_glassdoor_urls(urls):
    now = datetime.now().strftime('%Y-%m-%d')
    path = PROJECT_PATH / 'ingestion' / 'octoparse' / 'data' / 'companies' / f'glassdoor_urls_{now}.txt'
    file = open(path, 'w+')
    for url in urls:
        file.write(url + "\n")


def save_company_names(companies):
    now = datetime.now().strftime('%Y-%m-%d')
    path = PROJECT_PATH / 'ingestion' / 'octoparse' / 'data' / 'companies' / f'company_names_{now}.csv'
    companies_df = pd.DataFrame({'companies': companies})
    companies_df.to_csv(path, index=False)


if __name__ == '__main__':
    companies = fetch_companies()
    urls = generate_urls(companies)
    save_glassdoor_urls(urls)
    save_company_names(companies)
