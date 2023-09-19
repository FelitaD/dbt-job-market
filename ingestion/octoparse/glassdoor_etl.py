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


class GlassdoorETL:
    def __init__(self):
        self.companies_data = None
        self.company_names = None
        self.data = None

    def process(self):
        self.extract_latest_crawl()
        self.extract_company_names()
        self.concat_original_company_names()

        ## Verify companies match in concatenated dataframe
        # print(self.data.iloc[113]['URL'])
        # print(self.data.iloc[113])
        # print('\n')
        # print(self.data.iloc[4]['URL'])
        # print(self.data.iloc[4])
        # print('\n')
        # print(self.data.iloc[3]['URL'])
        # print(self.data.iloc[3])

        self.transform()
        self.insert_bigquery()

    def extract_latest_crawl(self):
        list_of_files = glob.glob(
            f'{PROJECT_PATH}/ingestion/octoparse/data/glassdoor/companies_*.csv')
        latest_file = max(list_of_files, key=os.path.getctime)
        self.companies_data = pd.read_csv(latest_file)

    def extract_company_names(self):
        list_of_files = glob.glob(
            f'{PROJECT_PATH}/ingestion/octoparse/data/glassdoor/company_names_*.csv')
        latest_file = max(list_of_files, key=os.path.getctime)
        self.company_names = pd.read_csv(latest_file)

    def concat_original_company_names(self):
        self.data = pd.concat([self.company_names, self.companies_data], axis=1)

    def transform(self):
        self.data = self.data.rename(columns={
            'companies': 'company_name',
            'URL': 'url',
            'Field1': 'rating',
            'Field2': 'name',
            'Field4': 'details',
            'Field5': 'headquarters',
            'Field6': 'stats',
        })
        self.data['rating'] = self.data['rating'].apply(lambda x: self.clean_rating(x))
        self.data[['industry', 'size']] = self.data['details'].apply(lambda x: self.split_details(x)).apply(pd.Series)
        self.data['headquarters'] = self.data['headquarters'].apply(lambda x: self.simplify_headquarters(x))
        self.data['stats_thousands'] = self.data['stats'].apply(lambda x: self.replace_thousands(x))
        self.data[['reviews', 'salaries', 'jobs']] = self.data['stats_thousands'].apply(
            lambda x: self.split_stats(x)).apply(pd.Series)

        self.data[['company_name', 'name', 'industry', 'size', 'headquarters', 'url']] = self.data[['company_name', 'name', 'industry', 'size', 'headquarters', 'url']].fillna('None')
        self.data[['rating', 'reviews', 'salaries', 'jobs']] = self.data[['rating', 'reviews', 'salaries', 'jobs']].fillna(0)

        self.data = self.data[['company_name', 'name', 'rating', 'industry', 'size', 'headquarters', 'reviews',
                               'salaries', 'jobs', 'url']]

    def insert_bigquery(self):
        custom_bq_client = bigquery.Client()

        engine = create_engine(
            'bigquery://complete-flag-399316/job-market?user_supplied_client=True',
            connect_args={'client': custom_bq_client},
        )
        with engine.connect() as connection:
            for i in range(len(self.data)):
                stmt = text(
                    "MERGE job_market.companies AS target "
                    "USING ("
                    "SELECT :company_name AS new_company_name "
                    ") AS source "
                    "ON target.company_name = source.new_company_name "
                    "WHEN MATCHED THEN "
                    "UPDATE SET target.company_name = source.new_company_name "  # DO NOTHING not supported by Bigquery
                    "WHEN NOT MATCHED THEN "
                    "INSERT (company_name, name, rating, industry, size, headquarters, reviews, salaries, jobs, url) "
                    "VALUES (:company_name, :name, :rating, :industry, :size, :headquarters, :reviews, :salaries, "
                    ":jobs, :url);")
                connection.execute(stmt,
                                   company_name=self.data['company_name'][i],
                                   name=self.data['name'][i],
                                   rating=self.data['rating'][i],
                                   industry=self.data['industry'][i],
                                   size=self.data['size'][i],
                                   headquarters=self.data['headquarters'][i],
                                   reviews=self.data['reviews'][i],
                                   salaries=self.data['salaries'][i],
                                   jobs=self.data['jobs'][i],
                                   url=self.data['url'][i]
                                   )

    @staticmethod
    def clean_rating(x):
        if pd.isna(x):
            return None
        return float(x.replace('★', '').strip())

    @staticmethod
    def split_details(x):
        if pd.isna(x):
            return [None, None]
        return x.split('\n') if '\n' in x else [None, x]

    @staticmethod
    def simplify_headquarters(x):
        if pd.isna(x):
            return None
        return x.split('Headquarters near ')[1]

    @staticmethod
    def replace_thousands(x):
        if pd.isna(x):
            return None
        return re.sub(r'(\d+)K', lambda m: str(int(m.group(1)) * 1000), x)

    @staticmethod
    def split_stats(x):
        if pd.isna(x):
            return [None, None, None]
        else:
            pattern = r"(\d+)\sReviews(\d+)\sSalaries(\d+)\sJobs"
            match = re.search(pattern, x)
            if match:
                return [int(match.group(1)), int(match.group(2)), int(match.group(3))]

if __name__ == '__main__':
    etl = GlassdoorETL()
    etl.process()
