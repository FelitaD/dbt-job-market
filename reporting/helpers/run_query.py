"""This module contains the interface to BigQuery.

It is handled by the bigquery Client module,
and Streamlit decorator `st.cache_data`.
"""

import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery

credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = bigquery.Client(credentials=credentials)


@st.cache_data(ttl=600)
def run_query(query):
    """Extracts data from BigQuery.

    Args:
        query: A SQL statement.

    Returns:
        A list of dictionaries.
    """
    query_job = client.query(query)
    rows_raw = query_job.result()
    # Convert to list of dicts. Required for st.cache_data to hash the return value.
    rows = [dict(row) for row in rows_raw]
    return rows
