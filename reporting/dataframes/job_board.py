import streamlit as st
import pandas as pd

from reporting.helpers.run_query import run_query
from reporting.helpers.queries import all_data_stmt
from reporting.helpers.filter_dataframe import filter_dataframe
from reporting.helpers.style_dataframe import highlight_row


def create_job_board():
    all_data_df = pd.DataFrame(run_query(all_data_stmt))

    job_board = st.dataframe(
        filter_dataframe(all_data_df).style
        .apply(highlight_row, axis=1)
        .format('{:.0f}', subset=['total_score', 'company_size', 'reviews_count', 'jobs_count', 'salaries_count']),
        use_container_width=True,
        column_order=(
            # 'rating_score',
            # 'seniority_score',
            'total_score',
            'created_at',
            'url_1',
            'title',
            'company',
            'industry',
            'stack',
            'remote',
            'location',
            'headquarters',
            'url',
            'is_same_glassdoor',
            # 'text',
            # 'contract',
            'company_size',
            'rating',
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
            'total_score': st.column_config.Column(width='small', label='🏆score'),
            # 'seniority_score': st.column_config.Column(width='small'),
            # 'rating_score': st.column_config.Column(width='small', label='📊rating score'),
            'title': st.column_config.Column(width='medium', label='👩‍💻title'),
            'company': st.column_config.Column(width='medium', label='💼company'),
            'stack': st.column_config.ListColumn(width='large', label='🛠️stack'),
            'text': st.column_config.Column(width='medium', label='📝job description'),
            'url_1': st.column_config.LinkColumn(width='small', label='🔗url'),
            'contract': st.column_config.Column(width='small', label='📜contract'),
            'created_at': st.column_config.DateColumn(width='small', label='📅created at'),
            'industry': st.column_config.Column(width='medium', label='🏭industry'),
            'remote': st.column_config.Column(width='small', label='🏠remote'),
            'location': st.column_config.Column(width='medium', label='🌍location'),
            'headquarters': st.column_config.Column(width='medium', label='🌍headquarters'),
            'url': st.column_config.LinkColumn(width='small', label='🔗url (glassdoor)'),
            'is_same_glassdoor': st.column_config.Column(width='small', label='⚠️is same glassdoor'),
            'rating': st.column_config.Column(width='small', label='⭐️rating'),
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
            # 'is_relevant': st.column_config.Column(width='small'),
        },
        height=800
    )
    return job_board
