import os
import re
import glob
import pandas as pd
import snowflake.connector

from config.definitions import PROJECT_PATH, SNOWFLAKE_ACCOUNT, SNOWFLAKE_ROLE, SNOWFLAKE_USER, SNOWSQL_PWD, WAREHOUSE


class GlassdoorETL:
    def __init__(self):
        self.data = None

    def process(self):
        self.extract_latest_crawl()
        self.transform()
        self.insert_snowflake()

    def extract_latest_crawl(self):
        list_of_files = glob.glob(
            f'{PROJECT_PATH}/ingestion/octoparse/data/glassdoor/*.csv')
        latest_file = max(list_of_files, key=os.path.getctime)
        self.data = pd.read_csv(latest_file)

    def transform(self):
        self.data = self.data.rename(columns={'URL': 'url',
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
        self.data[['reviews', 'salaries', 'jobs']] = self.data['stats_thousands'].apply(lambda x: self.split_stats(x)).apply(pd.Series)
        self.data = self.data[['name', 'rating', 'industry', 'size', 'headquarters', 'reviews', 'salaries', 'jobs', 'url']]
        self.data = self.data.rename(str.upper, axis='columns')

    def insert_snowflake(self):

        conn = snowflake.connector.connect(
            account=SNOWFLAKE_ACCOUNT,
            user=SNOWFLAKE_USER,
            password=SNOWSQL_PWD,
            database='ANALYTICS',
            schema='MARTS',
            role=SNOWFLAKE_ROLE,
            warehouse=WAREHOUSE
        )
        cur = conn.cursor()

        for i in range(len(self.data)):
            try:
                cur.execute(
                    "MERGE INTO companies AS target "
                    "USING ("
                    "SELECT %s AS NEW_URL "
                    ") AS source "
                    "ON target.URL = source.NEW_URL "
                    "WHEN MATCHED THEN "
                    "UPDATE SET target.URL = source.NEW_URL "  # DO NOTHING not supported by Snowflake
                    "WHEN NOT MATCHED THEN "
                    "INSERT (NAME, RATING, INDUSTRY, SIZE, HEADQUARTERS, REVIEWS, SALARIES, JOBS, URL) "
                    "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);",
                    (self.data['URL'][i],
                     self.data['NAME'][i], self.data['RATING'][i], self.data['INDUSTRY'][i], self.data['SIZE'][i],
                     self.data['HEADQUARTERS'][i], self.data['REVIEWS'][i], self.data['SALARIES'][i],
                     self.data['JOBS'][i], self.data['URL'][i]))
            except snowflake.connector.errors.ProgrammingError as e:
                # default error message
                print(e)
                # customer error message
                print('Error {0} ({1}): {2} ({3})'.format(e.errno, e.sqlstate, e.msg, e.sfqid))
        cur.close()

    @staticmethod
    def clean_rating(x):
        if pd.isna(x):
            return None
        return x.replace('★', '').strip()

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
                return [match.group(1), match.group(2), match.group(3)]


if __name__ == '__main__':
    etl = GlassdoorETL()
    etl.process()
    print(etl.data)
