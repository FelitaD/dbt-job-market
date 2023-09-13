import psycopg2
import logging

import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas

from config.definitions import JOB_MARKET_DB_PWD, JOB_MARKET_DB_USER

from config.definitions import SNOWFLAKE_ACCOUNT, SNOWFLAKE_ROLE, SNOWFLAKE_USER, SNOWSQL_PWD, WAREHOUSE


logging.basicConfig(filename='crawler_pipeline.log',
                    filemode='w',
                    format='%(asctime)s - %(message)s',
                    level=logging.INFO)


class JobsCrawlerPipeline:

    def __init__(self):
        self.conn = snowflake.connector.connect(
            account=SNOWFLAKE_ACCOUNT,
            user=SNOWFLAKE_USER,
            password=SNOWSQL_PWD,
            database='RAW',
            schema='PUBLIC',
            role=SNOWFLAKE_ROLE,
            warehouse=WAREHOUSE
        )

    def process_item(self, item, spider):
        """
        This function is called each time the spider scrapes an item.
        :param item:
        :param spider:
        :return: item
        """
        for field in item.fields:
            item.setdefault(field, 'NULL')
        cur = self.conn.cursor()
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
                    "INSERT (URL, TITLE, COMPANY, LOCATION, CONTRACT, INDUSTRY, TEXT, REMOTE, CREATED_AT) "
                    "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);",
                (item['url'][0], item['created_at'][0], item['url'][0],  item['title'][0], item['company'][0], item['location'][0], item['type'][0],
                 item['industry'][0], item['text'][0], item['remote'][0], item['created_at'][0]))
        except snowflake.connector.errors.ProgrammingError as e:
            # default error message
            print(e)
            # customer error message
            print('Error {0} ({1}): {2} ({3})'.format(e.errno, e.sqlstate, e.msg, e.sfqid))
        finally:
            cur.close()

        return item
