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

    st.dataframe(
        filter_dataframe(relevant_jobs_df).style
        .format('{:.1f}', subset=['rating'])
        .format('{:.0f}', subset=['reviews', 'total_score', 'rating_score']),
        column_config={
            'total_score': st.column_config.Column(width='small'),
            'is_relevant_score': st.column_config.Column(width='small'),
            'seniority_score': st.column_config.Column(width='small'),
            'is_same_glassdoor_score': st.column_config.Column(width='small'),
            'rating_score': st.column_config.Column(width='small'),
            "stack": st.column_config.ListColumn(width='medium'),
            "text": st.column_config.TextColumn(width='medium'),
            "size": st.column_config.TextColumn(width='small'),
            "job_url": st.column_config.LinkColumn(width='small'),
            "company_url": st.column_config.LinkColumn(width='small'),
        },
        height=800
    )

