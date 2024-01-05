import os
import re
import glob
import pandas as pd
import numpy as np
from sqlalchemy.engine import create_engine
from sqlalchemy import text
from google.cloud import bigquery

from config.definitions import PROJECT_PATH

pd.set_option('display.width', 300)
pd.set_option('display.max_columns', 15)


class GlassdoorETL:
    """Performs ETL on Glassdoor companies details.

    Details on companies were scraped on Glassdoor, based
    on a list of urls. To ensure its insertion in the table
    for the right company, we merge 2 dataframes to associate
    the original name and the url found on Glassdoor (might be
    different). It is transformed in order to be inserted
    (replace missing values to avoid clash in BigQuery...).
    """

    DATA_PATH = f'{PROJECT_PATH}/ingestion/octoparse/data/companies/'

    def __init__(self):
        """Contains DataFrames changing between ETL steps."""
        self.companies_data = None
        self.company_names = None
        self.data = None

    def process(self) -> None:
        """Factory function that performs the ETL process."""
        self.extract_latest_crawl()
        self.extract_company_names()
        self.concat_original_company_names()
        self.transform()
        self.insert_bigquery()

    def extract_latest_crawl(self) -> None:
        """Extracts Glassdoor data exported to a CSV."""
        list_of_files = glob.glob(f'{self.DATA_PATH}/companies*.csv')
        latest_file = max(list_of_files, key=os.path.getctime)
        self.companies_data = pd.read_csv(latest_file)

    def extract_company_names(self) -> None:
        """Gets company names to scrape from a CSV."""
        list_of_files = glob.glob(f'{self.DATA_PATH}/company_names_*.csv')
        latest_file = max(list_of_files, key=os.path.getctime)
        self.company_names = pd.read_csv(latest_file)

    def concat_original_company_names(self) -> None:
        """Reassemble companies' names and Glassdoor data into a DataFrame."""
        self.data = pd.concat([self.company_names, self.companies_data], axis=1)

    def transform(self) -> None:
        """Rename columns, replace missing values and cast to string."""
        self.data = self.data.rename(columns={
            'companies': 'company_name',
            'URL': 'url',
            'Field1': 'rating',
            'Field2': 'name',
            'Field3': 'details',
            'Field4': 'headquarters',
            'Field5': 'reviews',
            'Field6': 'salaries',
            'Field7': 'jobs',
        })
        self.data = self.data.fillna('None')
        self.data = self.data.astype('string')

    def insert_bigquery(self) -> None:
        """Insert transformed data in BigQuery."""
        custom_bq_client = bigquery.Client()

        engine = create_engine(
            'bigquery://resume-404711/job-market?user_supplied_client=True',
            connect_args={'client': custom_bq_client},
        )
        with engine.connect() as connection:
            for i in range(len(self.data)):
                stmt = text(
                    "MERGE job_market.stg_companies AS target "
                    "USING ("
                    "SELECT :company_name AS new_company_name "
                    ") AS source "
                    "ON target.company_name = source.new_company_name "
                    "WHEN MATCHED THEN "
                    "UPDATE SET target.company_name = source.new_company_name "  # DO NOTHING not supported by Bigquery
                    "WHEN NOT MATCHED THEN "
                    "INSERT (company_name, url, rating, name, details, headquarters, reviews, salaries, jobs) "
                    "VALUES (:company_name, :url, :rating, :name, :details, :headquarters, :reviews, :salaries, :jobs);")
                connection.execute(stmt,
                                   company_name=self.data['company_name'][i],
                                   url=self.data['url'][i],
                                   rating=self.data['rating'][i],
                                   name=self.data['name'][i],
                                   details=self.data['details'][i],
                                   headquarters=self.data['headquarters'][i],
                                   reviews=self.data['reviews'][i],
                                   salaries=self.data['salaries'][i],
                                   jobs=self.data['jobs'][i],
                                   )


if __name__ == '__main__':
    etl = GlassdoorETL()
    etl.process()

