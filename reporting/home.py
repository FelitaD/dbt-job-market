import streamlit as st
import altair as alt
import pandas as pd

from google.oauth2 import service_account
from google.cloud import bigquery

from helpers.queries import relevant_jobs_stmt, all_jobs_companies_stmt, techno_occurences_stmt


st.set_page_config(page_title="Data engineering job radar", page_icon="⛅︎", layout="wide")

credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = bigquery.Client(credentials=credentials)

tab1, tab2, tab3, tab4 = st.tabs(["Relevant jobs", "All jobs", "Technologies", "Companies"])


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
    # -------- DataFrame --------
    techno_occurences = run_query(techno_occurences_stmt)
    chart_data = st.data_editor(techno_occurences)

    # -------- Bar Chart --------

    df = pd.DataFrame({
        'Technos': [row['techno'] for row in techno_occurences],
        'Counts': [row['total'] for row in techno_occurences]
    })
    source = df[df['Counts'] > 5]
    print(source)

    c = alt.Chart(source).transform_joinaggregate(
        TotalCounts='sum(Counts)',
    ).transform_calculate(
        PercentOfTotal="datum.Counts / datum.TotalCounts"
    ).mark_bar().encode(
        alt.X('PercentOfTotal:Q').axis(format='.0%'),
        y='Technos:N'
    )

    st.altair_chart(c, use_container_width=True)
