from datetime import datetime, timedelta
import pandas as pd
import os
import glob
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas

from config.definitions import PROJECT_PATH, SNOWFLAKE_ACCOUNT, SNOWFLAKE_ROLE, SNOWFLAKE_USER, SNOWSQL_PWD, WAREHOUSE


class OctoparseETL:
    """
    Extract newly scraped jobs from octoparse, transform and insert into Snowflake.
    """

    def __init__(self, spider: str):
        self.spider = spider

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
    def parse_created_at(series):
        """
        Modifies information such as '1 week ago' to an actual date.
        """
        now = datetime.now()
        if 'hour' in series or 'heure' in series or 'minute' in series or 'second' in series:
            return now.strftime('%Y-%m-%d')
        if 'day' in series or 'jour' in series:
            for n in range(1, 8):
                if str(n) in series:
                    return (now - timedelta(days=n)).strftime('%Y-%m-%d')
        if 'week' in series or 'semaine' in series:
            for n in range(1, 5):
                if str(n) in series:
                    return (now - timedelta(weeks=n)).strftime('%Y-%m-%d')
        else:
            return series

    @staticmethod
    def insert_data_snowflake(data):
        """
        Automates the workflow of uploading data to a stage and then copying into a Snowflake table.
        """
        data = data.rename(str.upper, axis='columns')

        conn = snowflake.connector.connect(
            account=SNOWFLAKE_ACCOUNT,
            user=SNOWFLAKE_USER,
            password=SNOWSQL_PWD,
            database='RAW',
            schema='PUBLIC',
            role=SNOWFLAKE_ROLE,
            warehouse=WAREHOUSE
        )
        cur = conn.cursor()
        
        for i in range(len(data)):
            try:
                cur.execute(
                    "MERGE INTO job_postings AS target "
                    "USING ("
                    "SELECT %s AS NEW_URL, %s AS NEW_CREATED_AT"
                    ") AS source "
                    "ON target.URL = source.NEW_URL "
                    "WHEN MATCHED THEN "
                    "UPDATE SET target.CREATED_AT = source.NEW_CREATED_AT "
                    "WHEN NOT MATCHED THEN "
                    "INSERT (URL, TITLE, COMPANY, LOCATION, TEXT, CREATED_AT) "
                    "VALUES (%s,%s,%s,%s,%s,%s);",
                    (data['URL'][i], data['CREATED_AT'][i],
                     data['URL'][i], data['TITLE'][i], data['COMPANY'][i], data['LOCATION'][i], data['TEXT'][i], data['CREATED_AT'][i]))
            except snowflake.connector.errors.ProgrammingError as e:
                # default error message
                print(e)
                # customer error message
                print('Error {0} ({1}): {2} ({3})'.format(e.errno, e.sqlstate, e.msg, e.sfqid))
        cur.close()
