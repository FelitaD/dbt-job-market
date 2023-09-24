import streamlit as st
import time

st.set_page_config(layout='wide')

from reporting.charts.sankey import sankey_fig
from reporting.charts.treemap_technos import treemap_technos
from reporting.dataframes.technos_df import create_technos_st_df
from reporting.dataframes.job_board import create_job_board
from reporting.dataframes.companies_df import create_companies_st_df
from reporting.charts.scatter_companies import scatter_companies

tab_board, tab_charts, tab_data = st.tabs(['Job Board', 'Charts', 'Data'])


with st.sidebar:
    # Logo
    """
    ![logo](docs/radar.svg)
    """

    # Badges
    """
    [![Code](https://img.shields.io/badge/Code-000000?logo=github)](https://github.com/FelitaD/job-radar-2.0)
    """

    # Job board filters


with tab_board:
    create_job_board()

with tab_charts:
    st.plotly_chart(sankey_fig)
    st.plotly_chart(treemap_technos)
    st.plotly_chart(scatter_companies)
    # chart time series scores

with tab_data:
    create_technos_st_df()
    create_companies_st_df()
