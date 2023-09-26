import streamlit as st
import numpy as np

st.set_page_config(layout='wide')

from reporting.charts.sankey import sankey_fig
from reporting.charts.treemap_technos import treemap_technos
from reporting.dataframes.technos_df import create_technos_st_df
from reporting.helpers.filter_dataframe import DataframeFilter
from reporting.dataframes.job_board import create_job_board
from reporting.dataframes.companies_df import create_companies_st_df
from reporting.charts.scatter_companies import scatter_companies

tab_job_market, tab_me = st.tabs(['Data Engineering Job Market', 'About me'])

# Initialize dataframe filterer
df_filter = DataframeFilter()

with st.sidebar:
    st.markdown("<h1 style='text-align: center'>Job Radar</h1>", unsafe_allow_html=True)
    st.markdown("[![Code](https://img.shields.io/badge/Code-000000?logo=github)]"
                "(https://github.com/FelitaD/job-radar-2.0)")
    add_filters = st.checkbox('Add filters')

    if add_filters:
        # Slider widgets
        start_rating, end_rating = df_filter.create_slider('rating')
        start_reviews_count, end_reviews_count = df_filter.create_slider('reviews_count')
        print(start_reviews_count, end_reviews_count)
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

with tab_job_market:
    st.subheader("Job Board")

    if add_filters:
        st.write(f'Results contain {len(filtered_df)} rows')
        create_job_board(filtered_df)  # Filtered dataframe
    else:
        st.write(f'Results contain {len(df_filter.df)} rows')
        create_job_board(df_filter.df)  # Unfiltered dataframe

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
