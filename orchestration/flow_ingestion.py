from prefect import flow

from subflow_wttj import wttj_flow
from subflow_octoparse import octoparse_flow


@flow
def ingestion_flow(name='Ingestion Flow'):
    wttj_flow()
    octoparse_flow()


if __name__ == "__main__":
    # creates a deployment and stays running to monitor for work instructions generated on the server

    ingestion_flow.serve(name="ingestion-deployment")

