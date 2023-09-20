import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery

from helpers.filter_dataframe import filter_dataframe
from helpers.queries import relevant_jobs_stmt, all_jobs_companies_stmt, techno_occurences_stmt

st.set_page_config(page_title="Data engineering job radar", page_icon="⛅︎", layout="wide")

credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = bigquery.Client(credentials=credentials)

tab1, tab2, tab3 = st.tabs(["Relevant jobs", "All jobs", "Technologies"])


@st.cache_data(ttl=600)
def run_query(query):
    query_job = client.query(query)
    rows_raw = query_job.result()
    # Convert to list of dicts. Required for st.cache_data to hash the return value.
    rows = [dict(row) for row in rows_raw]
    return rows


with tab1:
    relevant_jobs = run_query(relevant_jobs_stmt)
    st.data_editor(
        relevant_jobs,
        column_config={
            "apply": st.column_config.CheckboxColumn(),
            "stack": st.column_config.ListColumn(width='medium'),
            "text": st.column_config.TextColumn(width='medium'),
            "size": st.column_config.TextColumn(width='small'),
            "job_url": st.column_config.LinkColumn(width='small'),
            "company_url": st.column_config.LinkColumn(width='small')
        }
    )


with tab2:
    all_jobs_companies = run_query(all_jobs_companies_stmt)
    st.dataframe(all_jobs_companies)


with tab3:
    techno_occurences = run_query(techno_occurences_stmt)
    chart_data = st.data_editor(techno_occurences)

    st.bar_chart(chart_data, x='techno', y='total')
