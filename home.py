"""This module is the main Streamlit script.

Typical usage:
    `streamlit run home.py`
"""

import numpy as np
import streamlit as st
import streamlit_analytics

from streamlit_timeline import timeline
from streamlit_elements import elements, mui, html, dashboard

# Must be called first
st.set_page_config(layout='wide')
streamlit_analytics.start_tracking()
streamlit_analytics.stop_tracking()


from reporting.charts.sankey import sankey_fig
from reporting.charts.treemap_technos import treemap_technos
from reporting.dataframes.technos_df import create_technos_st_df
from reporting.helpers.filter_dataframe import DataframeFilter
from reporting.dataframes.job_board import create_job_board
from reporting.dataframes.all_jobs_df import all_jobs_df
from reporting.dataframes.companies_df import create_companies_st_df
from reporting.charts.scatter_companies import scatter_companies

# Define layout elements
tab_job_board, tab_charts, tab_data, tab_hire_me = st.tabs(['🎯 Job Board', '📊 Charts', '🧮 Data', '👩🏻‍💻Resume Timeline'])

# Initialize dataframe filterer
df_filter = DataframeFilter()

with st.sidebar:
    st.markdown("<h1 style='text-align: center'>Job Radar</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:90%; text-align: center'>Search and compare data engineer positions</p>",
                unsafe_allow_html=True)
    st.markdown("<p align='center'><a href='https://github.com/FelitaD/job-radar-2.0'><img "
                "src='https://img.shields.io/badge/View_on_Github-000000?logo=github'></a></p>", unsafe_allow_html=True)

    add_filters = st.checkbox('Add Job Board filters')

    if add_filters:
        # Slider widgets
        start_rating, end_rating = df_filter.create_slider('rating')
        start_reviews_count, end_reviews_count = df_filter.create_slider('reviews_count')
        start_company_size, end_company_size = df_filter.create_slider('company_size')
        start_total_score, end_total_score = df_filter.create_slider('total_score')
        # Multiselect widgets
        created_at_filter = df_filter.create_multiselect('created_at')
        industry_filter = df_filter.create_multiselect('industry')
        stack_filter = df_filter.create_multiselect('stack')
        remote_filter = df_filter.create_multiselect('remote')

        # Create a filtered dataframe using widget default / user inputs
        filtered_df = df_filter.filter_dataframe(
            fields=['rating', 'reviews_count', 'company_size', 'total_score',
                    'created_at', 'industry', 'stack', 'remote'],
            start_rating=start_rating,
            end_rating=end_rating,
            start_reviews_count=start_reviews_count,
            end_reviews_count=end_reviews_count,
            start_company_size=start_company_size,
            end_company_size=end_company_size,
            start_total_score=start_total_score,
            end_total_score=end_total_score,
            created_at_filter=created_at_filter,
            industry_filter=industry_filter,
            stack_filter=stack_filter,
            remote_filter=remote_filter)

with tab_job_board:
    if add_filters:
        st.write(f'{len(filtered_df)} jobs')
        create_job_board(filtered_df)  # Filtered dataframe
    else:
        st.write(f'{len(df_filter.df)} jobs')
        create_job_board(df_filter.df)  # Unfiltered dataframe
    """
    - _score_: The sum of 2 hidden scores: the seniority level score + the company's glassdoor rating score.
    - _is_same_glassdoor_: Indicates if the company name collected on Glassdoor is the same as in the job posting. 
    If 0, manual verification is recommended.
    - _company_size_: The mean of the original data of the form '1 to 50 employees'.
    """

with tab_charts:
    # TODO: modify charts to be used in Streamlit Elements
    st.markdown('_New layout with streamlit-elements in progress._')
    st.subheader('Number of job postings during pipeline transformations')
    st.plotly_chart(sankey_fig)

    st.subheader('Occurence of technologies in job descriptions')
    st.plotly_chart(treemap_technos)

    st.subheader("Companies' Glassdoor rating, per number of reviews and company size")
    st.plotly_chart(scatter_companies)

with tab_data:
    st.subheader("Technologies")
    create_technos_st_df()
    """
    Technologies extracted from job descriptions. Their frequency is maximum 1 per job.  
    Categories, subcategories and descriptions come from the [MAD 2023](https://mad.firstmark.com/), omitting the categories "Applications - *".
    """

    st.subheader("Companies")
    create_companies_st_df()
    """
    Data scraped on Glassdoor each time a new company is added to the `jobs` table.
    """

    st.subheader('All jobs')
    st.dataframe(all_jobs_df)
    """
    Data after technologies extraction and before relevancy filtering.
    """

with tab_hire_me:
    with open('docs/timeline.json', "r") as f:
        data = f.read()

    # TODO: make the years appear completely at the bottom
    timeline(data, height=800)
    """
    Events are categorized as _academic_, _work_ and _certificates_ for easier navigation.
    My [Github Portfolio](https://github.com/FelitaD/Portfolio) contains projects and other online courses.
    """

