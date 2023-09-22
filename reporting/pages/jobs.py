import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Jobs", layout="wide")

from reporting.home import run_query
from reporting.helpers.queries import relevant_jobs_stmt, all_data_stmt
from reporting.helpers.filter_dataframe import filter_dataframe

all_data_df = pd.DataFrame(run_query(all_data_stmt))
ordered_df = all_data_df[all_data_df['is_relevant_score'] == 1].sort_values(by=['total_score'], ascending=False)

st.dataframe(
    filter_dataframe(ordered_df),
    use_container_width=True,
    column_order=(
        'title',
        'company',
        'stack',
        'text',
        'url_1',
        'seniority_score',
        'contract',
        'created_at',
        'industry',
        'remote',
        'location',
        'headquarters',
        'is_same_glassdoor_score',
        'url',
        'rating_score',
        'rating',
        'company_size',
        'reviews_count',
        'jobs_count',
        'salaries_count',
        'id',
        # 'industry_1',
        # 'company_name',
        # 'name',
        # 'id_1',
        # 'total_score',
        # 'is_relevant_score',
    ),
    column_config={
        'title': st.column_config.Column(width='medium', label='👩‍💻title'),
        'company': st.column_config.Column(width='medium', label='💼company'),
        'stack': st.column_config.ListColumn(width='medium', label='🛠️stack'),
        'text': st.column_config.Column(width='medium', label='📝job description'),
        'url_1': st.column_config.LinkColumn(width='small', label='🔗url (listing)'),
        'seniority_score': st.column_config.Column(width='small'),
        'contract': st.column_config.Column(width='small', label='📜contract'),
        'created_at': st.column_config.DateColumn(width='small', label='📅created at'),
        'industry': st.column_config.Column(width='medium', label='🏭industry'),
        'remote': st.column_config.Column(width='small', label='🏠remote'),
        'location': st.column_config.Column(width='medium', label='🌍location'),
        'headquarters': st.column_config.Column(width='medium', label='🌍headquarters'),
        'url': st.column_config.LinkColumn(width='small', label='🔗url (glassdoor)'),
        'is_same_glassdoor_score': st.column_config.Column(width='small', label='⚠️is same glassdoor'),
        'rating': st.column_config.Column(width='small', label='⭐️rating'),
        'rating_score': st.column_config.Column(width='small', label='📊rating score'),
        'company_size': st.column_config.Column(width='small', label='👥size'),
        'reviews_count': st.column_config.Column(width='small', label='📊reviews count'),
        'jobs_count': st.column_config.Column(width='small', label='📊jobs count'),
        'salaries_count': st.column_config.Column(width='small', label='📊salaries count'),
        'id': st.column_config.Column(width='small'),
        # 'industry_1': st.column_config.Column(width='medium'),
        # 'company_name': st.column_config.Column(width='medium'),
        # 'name': st.column_config.Column(width='medium'),
        # 'id_1': st.column_config.Column(width='small'),
        # 'total_score': st.column_config.Column(width='small'),
        # 'is_relevant_score': st.column_config.Column(width='small'),
    },
    height=800
)
