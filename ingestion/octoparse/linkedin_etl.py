"""This module performs an ETL process.

Data sources are csv files, transformation with pandas
and loading database is BigQuery.
"""
import datetime
import pandas as pd
import numpy as np
import os
import glob
import logging

from sqlalchemy.engine import create_engine
from sqlalchemy import text
from google.cloud import bigquery
from pandas import DataFrame, Series

from config.definitions import PROJECT_PATH
from config.logging_config import logger


class LinkedinETL:
    """ETL for jobs scraped from LinkedIn.

    Transforms a csv file into a dataframe that can be
    inserted into BigQuery.
    """

    def __init__(self, spider: str):
        """Initializes the LinkedinETL instance.

        Args:
            spider: A string of the spider name.
        """
        self.spider = spider
        self.data_path = PROJECT_PATH / 'ingestion' / 'octoparse' / 'data' / self.spider

    def process(self) -> None:
        """Factory function that performs the ETL process."""
        raw = self.extract_latest_crawl()
        print(f'Raw data: {len(raw)} rows')
        transformed_generic = self.transform_generic(raw)
        print(f'Transformed generic data: {len(transformed_generic)} rows')
        transformed_date_posted = self.transform_date_posted(transformed_generic)
        print(f'Transformed date data: {len(transformed_date_posted)} rows')
        transformed_date_posted = transformed_date_posted[['url', 'title', 'company', 'location', 'text', 'created_at']]
        self.insert_bigquery(transformed_date_posted)

    def extract_latest_crawl(self) -> DataFrame:
        """Extracts data from the latest csv file in the spider folder.

        Returns:
            A dataframe with spider's scraped data.
        """
        print(f'Extracting latest crawl for {self.spider}')
        list_of_files = glob.glob(f'{self.data_path}/*.csv')
        latest_file = max(list_of_files, key=os.path.getctime)
        return pd.read_csv(latest_file)

    @staticmethod
    def transform_generic(data: pd.DataFrame = None) -> DataFrame:
        """Performs general transformations.

        Lower column names, strip cells and remove
        rows where `url` or `text` is missing.

        Args:
            data: A dataframe with raw data.

        Returns:
            A clean dataframe.
        """
        # Rename columns to small letters
        data = data.rename(str.lower, axis='columns')
        # Remove whitespaces
        data = data.apply(lambda x: x.str.strip())
        # Drop rows that don't respect NOT NULL constraint on url and text
        data = data.replace('', np.nan)
        data = data.dropna(subset=['url', 'text'])
        # Reset index
        data = data.reset_index(drop=True)
        return data

    def transform_date_posted(self, data: DataFrame) -> DataFrame:
        """Transforms date information to datetime objects.

        Returns:
            A dataframe with a date column
        """
        data['created_at'] = data['date_posted'].apply(lambda x: self.parse_created_at(x))

        return data

    @staticmethod
    def parse_created_at(row: str) -> datetime.date:
        """Modifies information such as '1 week ago' to an actual date.

        Returns:
            A date object.
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

    @staticmethod
    def insert_bigquery(data: DataFrame) -> None:
        """Insert formatted data in BigQuery.

        Returns:
            None. If using `fetchall()`, it returns all rows
            contained in the table.
        """
        custom_bq_client = bigquery.Client()
        engine = create_engine(
            'bigquery://resume-404711/job-market?user_supplied_client=True',
            connect_args={'client': custom_bq_client},
            echo=True
        )
        with engine.connect() as connection:
            for i in range(len(data)):
                stmt = text(
                    "MERGE job_market.raw_job_postings target "
                    "USING ( SELECT :url AS new_url, :created_at AS new_created_at) source "
                    "ON target.url = source.new_url "
                    "WHEN MATCHED THEN "
                    "UPDATE SET target.created_at = source.new_created_at "
                    "WHEN NOT MATCHED THEN "
                    "INSERT (url, title, company, location, text, created_at) "
                    "VALUES (:url, :title, :company, :location, :text, :created_at) "
                    ";")
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
    etl = LinkedinETL(spider='linkedin_fr_all')
    etl.process()
