import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery

from helpers.queries import relevant_jobs_stmt, all_jobs_companies_stmt, techno_occurences_stmt, all_companies_stmt


st.set_page_config(page_title="Data engineering job radar", page_icon="⛅︎", layout="wide")

credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = bigquery.Client(credentials=credentials)


@st.cache_data(ttl=600)
def run_query(query):
    query_job = client.query(query)
    rows_raw = query_job.result()
    # Convert to list of dicts. Required for st.cache_data to hash the return value.
    rows = [dict(row) for row in rows_raw]
    return rows

