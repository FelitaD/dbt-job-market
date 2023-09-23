import pandas as pd
import streamlit as st

from reporting.helpers.run_query import run_query
from reporting.helpers.queries import companies_stmt

companies_df = pd.DataFrame(run_query(companies_stmt))


def create_companies_st_df():
    st.data_editor(companies_df.sort_values(by=['company_name']),
                   use_container_width=True,
                   column_config={
                       "company_name": st.column_config.TextColumn('name (listing)'),
                       "name": st.column_config.TextColumn('name (glassdoor)'),
                       "url": st.column_config.LinkColumn('url', width='small'),
                       "industry": st.column_config.Column(),
                       "headquarters": st.column_config.Column(),
                       "rating": st.column_config.Column(),
                       "company_size": st.column_config.NumberColumn('size mean'),
                       "reviews_count": st.column_config.NumberColumn(),
                       "jobs_count": st.column_config.NumberColumn(),
                       "salaries_count": st.column_config.NumberColumn(),
                   })
