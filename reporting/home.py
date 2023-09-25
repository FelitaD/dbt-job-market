import streamlit as st
import numpy as np

st.set_page_config(layout='wide')

from reporting.charts.sankey import sankey_fig
from reporting.charts.treemap_technos import treemap_technos
from reporting.dataframes.technos_df import create_technos_st_df
from reporting.helpers.filter_dataframe import create_slider, filter_dataframe, create_multiselect, create_unfiltered_df
from reporting.dataframes.job_board import create_job_board
from reporting.dataframes.companies_df import create_companies_st_df
from reporting.charts.scatter_companies import scatter_companies

tab_job_market, tab_me = st.tabs(['Data Engineering Job Market', 'About me'])


with st.sidebar:
    # Title
    st.markdown("<h1 style='text-align: center'>Job Radar</h1>", unsafe_allow_html=True)

    # Logo
    # st.image('docs/logo.png')

    # Badges
    """
    [![Code](https://img.shields.io/badge/Code-000000?logo=github)](https://github.com/FelitaD/job-radar-2.0)
    """

    # Content
    st.write('On this page')
    st.markdown("""
        [Job Board](#job_board)  
        [Charts](#charts)  
        [Data](#data)
    """)

    # Filters
    # start_rating, end_rating = create_slider('rating')
    # start_reviews_count, end_reviews_count = create_slider('reviews_count')
    # start_company_size, end_company_size = create_slider('company_size')
    # start_total_score, end_total_score = create_slider('total_score')
    # created_at_filter = create_multiselect('created_at')
    # industry_filter = create_multiselect('industry')
    # stack_filter = create_multiselect('stack')
    # remote_filter = create_multiselect('remote')


with tab_job_market:
    st.subheader("Job Board", anchor='job_board')
    # filtered_df = filter_dataframe(['rating', 'reviews_count', 'company_size', 'total_score', 'created_at',
    #                                 'industry', 'stack', 'remote'],
    #                                start_rating=start_rating,
    #                                end_rating=end_rating,
    #                                start_reviews_count=start_reviews_count,
    #                                end_reviews_count=end_reviews_count,
    #                                start_company_size=start_company_size,
    #                                end_company_size=end_company_size,
    #                                start_total_score=start_total_score,
    #                                end_total_score=end_total_score,
    #                                created_at_filter=created_at_filter,
    #                                industry_filter=industry_filter,
    #                                stack_filter=stack_filter,
    #                                remote_filter=remote_filter)
    df = create_unfiltered_df()
    st.write(f'Your query produced {len(df)} rows')
    create_job_board(df)

    st.subheader("Charts")
    st.plotly_chart(sankey_fig)
    st.plotly_chart(treemap_technos)
    st.plotly_chart(scatter_companies)
    # chart time series scores

    st.subheader("Data")
    create_technos_st_df()
    create_companies_st_df()

with tab_me:
    st.markdown("Timeline")
