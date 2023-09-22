import streamlit as st
import plotly.express as px
import pandas as pd

from reporting.home import run_query
from reporting.helpers.queries import companies_stmt, all_data_stmt


companies_df = pd.DataFrame(run_query(companies_stmt))

# Chart: companies rating per reviews and size

st.subheader('Companies Glassdoor rating per number of reviews and company size')
fig = px.scatter(companies_df[companies_df.company_size.notnull()], x="reviews_count", y="rating", size='company_size',
                 log_x=True, height=600, template='plotly_dark',
                 marginal_x="box", marginal_y="box")
st.plotly_chart(fig, use_container_width=True)

# Data

st.subheader('Data')
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
