from prefect import flow, task, Flow
from prefect_shell import ShellOperation
from prefect.task_runners import SequentialTaskRunner

from config.definitions import PROJECT_PATH
from helpers.s3_helper import S3Helper


@flow
def wttj_flow(name='Wttj Flow'):
    """
    This flow parses welcometothejungle.com sequentially.
    The spiders tasks call the script directly from command line.
    """
    # Scrape dynamic pages for job postings' links
    # scrape_wttj_links()
    # Stores links to S3
    # upload_links_to_s3()
    # Scrape static pages
    scrape_wttj_job_details()


@task
def scrape_wttj_links():
    ShellOperation(
        commands=[
            "python3 crawler/scrapy/spiders/wttj_links.py"
        ],
        working_dir=f"{PROJECT_PATH}"
    ).run()

@task
def upload_links_to_s3():
    S3Helper().upload_to_s3()


@task
def scrape_wttj_job_details():
    ShellOperation(
        commands=[
            "python3 crawler/scrapy/spiders/wttj.py"
        ],
        working_dir=f"{PROJECT_PATH}"
    ).run()
