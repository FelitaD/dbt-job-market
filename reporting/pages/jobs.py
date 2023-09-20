import streamlit as st
import altair as alt
import pandas as pd

from reporting.home import client, run_query
from reporting.helpers.queries import relevant_jobs_stmt, all_jobs_companies_stmt

tab_data, tab_charts = st.tabs(['Data', 'Charts'])


with tab_data:
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

    all_jobs_companies = run_query(all_jobs_companies_stmt)
    st.dataframe(all_jobs_companies)