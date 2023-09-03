from datetime import datetime, timedelta
from prefect import flow, task, get_run_logger
from prefect.tasks import task_input_hash
import sqlalchemy
from sqlalchemy import create_engine
import pandas as pd
import glob
import os
import psycopg2

from config.definitions import DB_STRING, PROJECT_PATH


def extract_latest_crawl(spider: str = 'linkedin_eu_remote'):
    list_of_files = glob.glob(f'{PROJECT_PATH}/octoparse-data/{spider}/*')  # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file, pd.read_csv(latest_file)

def transform_data(data: pd.DataFrame = None):
    data.rename(str.lower, axis='columns', inplace=True)
    df_obj = data.select_dtypes(['object'])
    data[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())
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

def insert_data(data, db: sqlalchemy.engine.base.Engine, query: str, parameters: dict):
    log_headline: str = "insert_data() ::"
    stmt = sqlalchemy.text(query)

    try:
        with db.connect() as conn:
            conn.execute(stmt, parameters=parameters)
            conn.commit()
        print(f"{log_headline} OK inserted data ")
    except Exception as e:
        print(f"{log_headline} Error {e}")


def linkedin_eu_remote():
    # logger = get_run_logger()

    file, raw = extract_latest_crawl()
    # logger.info(f'\n ------- Data for latest crawl {file}: ------- \n')

    transformed = transform_data(raw)
    # logger.info('\n  ------- Tranformed data: ------- \n')

    # logger.info('\n  ------- Loading data... ------- \n')
    engine = create_engine(DB_STRING, echo=True)
    query = "INSERT INTO raw_jobs (url, title, company, location, text, created_at) VALUES (:url, :title, :company, :location, :text, :created_at)"
    for i in range(len(transformed)):
        parameters = {
            'url': transformed['url'].iloc[i],
            'title': transformed['title'].iloc[i],
            'company': transformed['company'].iloc[i],
            'location': transformed['location'].iloc[i],
            'text': transformed['text'].iloc[i],
            'created_at': transformed['created_at'].iloc[i]
            }
        insert_data(data=transformed, db=engine, query=query, parameters=parameters)

if __name__ == '__main__':
    linkedin_eu_remote()