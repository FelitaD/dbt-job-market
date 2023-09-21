import psycopg2
import logging

from sqlalchemy.engine import create_engine
from sqlalchemy import text
from google.cloud import bigquery


logging.basicConfig(filename='crawler_pipeline.log',
                    filemode='w',
                    format='%(asctime)s - %(message)s',
                    level=logging.INFO)


class JobsCrawlerPipeline:

    def process_item(self, item, spider):
        """
        This function is called each time the spider scrapes an item.
        :param item:
        :param spider:
        :return: item
        """
        for field in item.fields:
            item.setdefault(field, 'NULL')
            
        custom_bq_client = bigquery.Client()
        engine = create_engine(
            'bigquery://complete-flag-399316/job-market?user_supplied_client=True',
            connect_args={'client': custom_bq_client},
        )
        
        with engine.connect() as connection:
            stmt = text(
                "MERGE job_market.raw_job_postings target "
                "USING ( SELECT :url AS new_url, :created_at AS new_created_at) source "
                "ON target.url = source.new_url "
                "WHEN MATCHED THEN "
                "UPDATE SET target.url = source.new_url "
                "WHEN NOT MATCHED THEN "
                "INSERT (url, title, company, location, contract, industry, text, remote, created_at) "
                "VALUES (:url, :title, :company, :location, :contract, :industry, :text, :remote, :created_at);")
            connection.execute(stmt,
                               url=item['url'][0],
                               title=item['title'][0],
                               company=item['company'][0],
                               location=item['location'][0],
                               contract=item['contract'][0],
                               industry=item['industry'][0],
                               text=item['text'][0],
                               remote=item['remote'][0],
                               created_at=item['created_at'][0],
                               )
            return item
