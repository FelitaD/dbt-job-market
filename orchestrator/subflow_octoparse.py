from prefect import flow, task


@flow
def octoparse_flow():
    # Octoparse etl Subflow
    # - Wait scheduled run at 6 pm
    # task - etl Linkedin EU remote jobs
    # task - etl pipeline automatically uploads to Snowflake
    pass

@task
def open_octoparse():
    pass
