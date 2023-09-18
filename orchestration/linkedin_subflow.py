from prefect import flow, task

from ingestion.octoparse.linkedin_etl import LinkedinETL


@flow
def linkedin_flow():
    linkedin_etl(spider='linkedin_eu_remote')
    linkedin_etl(spider='linkedin_fr_all')


@task(log_prints=True)
def linkedin_etl(spider):
    etl = LinkedinETL(spider=spider)
    etl.process()


