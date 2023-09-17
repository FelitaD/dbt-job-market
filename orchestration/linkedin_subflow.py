from prefect import flow, task

from ingestion.octoparse.linkedin_etl import LinkedinETL


@flow
def linkedin_flow():
    linkedin_etl(spider='linkedin_eu_remote')
    linkedin_etl(spider='linkedin_fr_all')


@task(log_prints=True)
def linkedin_etl(spider):
    etl = LinkedinETL(spider=spider)

    file, raw = etl.extract_latest_crawl()

    transformed_generic = etl.transform_generic(raw)
    transformed_date_posted = etl.transform_date_posted(transformed_generic)

    etl.insert_snowflake(transformed_date_posted)


if __name__ == '__main__':
    linkedin_flow()
