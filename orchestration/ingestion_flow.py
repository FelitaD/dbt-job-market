from prefect import flow

from wttj_subflow import wttj_flow
from linkedin_subflow import linkedin_flow


@flow
def ingestion_flow(name='Ingestion Flow'):
    wttj_flow()
    linkedin_flow()


if __name__ == "__main__":
    # creates a deployment and stays running to monitor for work instructions generated on the server
    ingestion_flow.serve(name="ingestion-deployment")
