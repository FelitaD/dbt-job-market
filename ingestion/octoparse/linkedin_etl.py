import datetime
import pandas as pd
import os
import glob
from sqlalchemy.engine import create_engine
from sqlalchemy.schema import Table
from sqlalchemy import text
from google.cloud import bigquery


from config.definitions import PROJECT_PATH


class LinkedinETL:
    """
    Extract newly scraped jobs from octoparse, transform and insert into Snowflake / Bigquery (after migration).
    """

    def __init__(self, spider: str):
        self.spider = spider

    def process(self):
        file, raw = self.extract_latest_crawl()
        transformed_generic = self.transform_generic(raw)
        transformed_date_posted = self.transform_date_posted(transformed_generic)
        self.insert_bigquery(transformed_date_posted)

    def extract_latest_crawl(self):
        list_of_files = glob.glob(
            f'{PROJECT_PATH}/ingestion/octoparse/data/{self.spider}/*.csv')
        latest_file = max(list_of_files, key=os.path.getctime)
        return latest_file, pd.read_csv(latest_file)

    def transform_generic(self, data: pd.DataFrame = None):
        """
        Generic transformation: remove missing values, remove whitespaces.
        """
        # Rename columns to small letters
        data = data.rename(str.lower, axis='columns')

        # Drop columns that don't respect NOT NULL constraint
        data = data.dropna(subset=['url', 'text'])

        # Remove whitespaces in string columns
        df_obj = data.select_dtypes(['object'])
        data[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())

        # Reset index
        data = data.reset_index(drop=True)

        return data

    def transform_date_posted(self, data):
        """
        Transform date information to datetime objects.
        """
        data['created_at'] = data['date_posted'].apply(lambda x: self.parse_created_at(x))

        return data[['url', 'title', 'company', 'location', 'text', 'created_at']]

    @staticmethod
    def parse_created_at(row):
        """
        Modifies information such as '1 week ago' to an actual date.
        """
        today = datetime.date.today()
        if 'hour' in row or 'heure' in row or 'minute' in row or 'second' in row:
            return today
        if 'day' in row or 'jour' in row:
            for n in range(1, 8):
                if str(n) in row:
                    return today - datetime.timedelta(days=n)
        if 'week' in row or 'semaine' in row:
            for n in range(1, 5):
                if str(n) in row:
                    return today - datetime.timedelta(weeks=n)
        return row

    @staticmethod
    def insert_bigquery(data):

        custom_bq_client = bigquery.Client()

        engine = create_engine(
            'bigquery://complete-flag-399316/job-market?user_supplied_client=True',
            connect_args={'client': custom_bq_client},
        )
        with engine.connect() as connection:

            for i in range(len(data)):
                stmt = text(
                    "MERGE job_market.job_postings target "
                    "USING ( SELECT :url AS new_url, :created_at AS new_created_at) source "
                    "ON target.url = source.new_url "
                    "WHEN MATCHED THEN "
                    "UPDATE SET target.created_at = source.new_created_at "
                    "WHEN NOT MATCHED THEN "
                    "INSERT (url, title, company, location, text, created_at) "
                    "VALUES (:url, :title, :company, :location, :text, :created_at);")
                connection.execute(stmt,
                                   url=data['url'][i],
                                   created_at=data['created_at'][i],
                                   title=data['title'][i],
                                   company=data['company'][i],
                                   location=data['location'][i],
                                   text=data['text'][i],
                                   )


if __name__ == '__main__':
    etl = LinkedinETL(spider='linkedin_eu_remote')
    etl.process()
