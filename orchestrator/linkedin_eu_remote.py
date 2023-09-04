from datetime import datetime, timedelta
from prefect import flow, task, get_run_logger
from prefect.tasks import task_input_hash
import sqlalchemy
from sqlalchemy import create_engine
import pandas as pd
import glob
import os
import psycopg2
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas



from config.definitions import DB_STRING, PROJECT_PATH, SNOWFLAKE_ACCOUNT, SNOWFLAKE_ROLE, SNOWFLAKE_USER, SNOWSQL_PWD, WAREHOUSE


def extract_latest_crawl(spider: str = 'linkedin_eu_remote'):
    list_of_files = glob.glob(f'{PROJECT_PATH}/octoparse-data/{spider}/*')  # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file, pd.read_csv(latest_file)

def transform_data(data: pd.DataFrame = None):
    """
    Processes raw data before inserting into database.
    """
    # Rename columns to small letters
    data = data.rename(str.lower, axis='columns')

    # Drop columns that don't respect NOT NULL constraint
    data = data.dropna(subset=['url', 'text'])

    # Remove whitespaces in string columns
    df_obj = data.select_dtypes(['object'])
    data[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())

    # Change column with date information (eg. "1 week ago") to datetime objects
    data['created_at'] = data['date_posted'].apply(lambda x: parse_created_at(x))
    data['created_at'] = pd.to_datetime(data['created_at']).apply(lambda x: x.strftime('%Y-%m-%d'))

    return data[['url', 'title', 'company', 'location', 'text', 'created_at']]

@staticmethod
def parse_created_at(series):
    now = datetime.now()
    if 'hours' in series:
        return now
    if 'day' in series:
        for n in range(1,8):
            if str(n) in series:
                return now - timedelta(days=n)
    if 'week' in series:
        for n in range(1,5):
            if str(n) in series:
                return now - timedelta(weeks=n)


def insert_data_snowflake(data):
    """
    Automates the workflow of uploading data to a stage and then copying into a Snowflake table.
    """
    data.rename(str.upper, axis='columns', inplace=True)
    cnx = snowflake.connector.connect(
        account=SNOWFLAKE_ACCOUNT,
        user=SNOWFLAKE_USER,
        password=SNOWSQL_PWD,
        database='RAW',
        schema='PUBLIC',
        role=SNOWFLAKE_ROLE,
        warehouse=WAREHOUSE
    )
    success, nchunks, nrows, output = write_pandas(cnx, data, 'JOB_POSTINGS')
    print(f'Insertion: {success}, '
          f'Number of chunks inserted: {nchunks}, '
          f'Number of rows inserted: {nrows}, '
          f'Inserted data: {output}')


def linkedin_eu_remote():
    # logger = get_run_logger()

    file, raw = extract_latest_crawl()
    # logger.info(f'\n ------- Data for latest crawl {file}: ------- \n')

    transformed = transform_data(raw)
    # logger.info('\n  ------- Tranformed data: ------- \n')

    # logger.info('\n  ------- Inserted data: ------- \n')
    insert_data_snowflake(transformed)

if __name__ == '__main__':
    linkedin_eu_remote()