import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery


credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = bigquery.Client(credentials=credentials)

tab_welcome, tab_doc = st.tabs(['Welcome', 'Project Documentation'])


@st.cache_data(ttl=30)
def run_query(query):
    query_job = client.query(query)
    rows_raw = query_job.result()
    # Convert to list of dicts. Required for st.cache_data to hash the return value.
    rows = [dict(row) for row in rows_raw]
    return rows


with tab_welcome:
    st.write('Welcome :rocket:')

with tab_doc:
    st.markdown(
        """
        # Job Radar 2.0
    
        Version 2 of [Job Radar 1.0](https://github.com/FelitaD/job-radar-1.0) by modifying technologies used.
        
        Focus is emphasized on analytics engineering using [Snowflake](https://www.snowflake.com/en/) coupled with [dbt](https://www.getdbt.com/) 
        and visualisations in Looker Studio and Streamlit. Orchestration with Prefect. Data modeling with Data Vault.
    
        """
    )
    # st.components.v1.html(
    #     """
    #     <iframe width="968" height="632" src="https://miro.com/app/live-embed/uXjVMNceW10=/?moveToViewport=-492,5651,4500,1505&embedId=45852963792" frameborder="0" scrolling="no" allow="fullscreen; clipboard-read; clipboard-write" allowfullscreen></iframe>
    #     """,
    #     width=1000,
    #     height=600
    # )
    # st.components.v1.html(
    #     """
    #     <iframe width="560" height="315" src='https://dbdiagram.io/embed/65083b9d02bd1c4a5ec730d7'> </iframe>
    #     """,
    #     width=1000,
    #     height=600
    # )
