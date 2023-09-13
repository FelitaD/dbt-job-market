from prefect import flow, task

from ingestion.octoparse.octoparse_etl import OctoparseETL


@flow
def octoparse_flow():
    linkedin_etl(spider='linkedin_eu_remote')
    linkedin_etl(spider='linkedin_fr_all')


@task(log_prints=True)
def linkedin_etl(spider):
    etl = OctoparseETL(spider=spider)

    file, raw = etl.extract_latest_crawl()

    transformed_generic = etl.transform_generic(raw)
    transformed_date_posted = etl.transform_date_posted(transformed_generic)

    etl.insert_data_snowflake(transformed_date_posted)


if __name__ == '__main__':
    octoparse_flow()