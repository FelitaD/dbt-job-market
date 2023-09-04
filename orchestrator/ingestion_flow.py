from prefect import Flow, task
from prefect_shell import ShellOperation

from config.definitions import PROJECT_PATH
from helpers.s3_helper import S3Helper
# Crawler Flow

# Scrapy crawler Subflow


# Octoparse etl Subflow
# - Wait scheduled run at 6 pm
# task - etl Linkedin EU remote jobs
# task - etl pipeline automatically uploads to Snowflake

@task
scrape_wttj_links = ShellOperation(
        commands=[
            "python3 crawler/scrapy-crawler/spiders/wttj_links.py"
        ],
        working_dir=f"{PROJECT_PATH}"
    ).run()

S3Helper().upload_to_s3()

with Flow("Scrapy Flow") as f:
    # task - scrape wttj links
    scrape_wttj_links = task(command='python3 crawler/scrapy-crawler/spiders/wttj_links.py')
    # task - upload to s3
    # task - scrape wttj jobs
    # - scrapy pipeline automatically uploads to Snowflake

out = f.run()
print(out)

# dbt deployment
# - Check dbt deployment

# Streamlit
# - Run streamlit app
