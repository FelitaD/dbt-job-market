import streamlit as st
import altair as alt
import pandas as pd
import datetime

st.set_page_config(page_title="Jobs", layout="wide")

from reporting.home import run_query
from reporting.helpers.queries import relevant_jobs_stmt
from reporting.helpers.filter_dataframe import filter_dataframe
from reporting.helpers.style_dataframe import (highlight_title, highlight_quant_column)

tab_charts, tab_data, tab_raw_data = st.tabs(['Charts', 'Data', 'Raw data'])


with tab_data:
    relevant_jobs = run_query(relevant_jobs_stmt)
    relevant_jobs_df = pd.DataFrame(relevant_jobs)
    print(relevant_jobs_df)

    st.dataframe(
        filter_dataframe(relevant_jobs_df).style
        .apply(highlight_title, axis=1, subset=['title'])
        .apply(highlight_quant_column, subset=['rating'])
        .format('{:.1f}', subset=['rating'])
        .format('{:.0f}', subset=['reviews']),
        column_config={
            "stack": st.column_config.ListColumn(width='medium'),
            "text": st.column_config.TextColumn(width='medium'),
            "size": st.column_config.TextColumn(width='small'),
            "job_url": st.column_config.LinkColumn(width='small'),
            "company_url": st.column_config.LinkColumn(width='small'),
        },
        height=800
    )
