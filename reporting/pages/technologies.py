import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Technologies", layout="wide")

from reporting.home import client, run_query
from reporting.helpers.queries import technos_stmt


technos_df = pd.DataFrame(run_query(technos_stmt))

# Chart
st.subheader('Technologies occurrences in job descriptions')
fig = px.treemap(technos_df, path=['category', 'subcategory', 'techno'], values='total',
                 hover_data={'category': False, 'subcategory': False, 'techno': False, 'description': False},
                 height=800, color='category', color_discrete_sequence=px.colors.qualitative.Pastel)
st.plotly_chart(fig, use_container_width=True)

# Data
st.subheader('Data')
st.data_editor(technos_df,
               use_container_width=True,
               column_order=('total', 'techno', 'category', 'subcategory', 'description'),
               column_config={
                   'total': st.column_config.Column(width='small', label='total'),
                   'techno': st.column_config.Column(label='techno name'),
                   'category': st.column_config.Column(),
                   'subcategory': st.column_config.Column(),
                   'description': st.column_config.Column(),
               })
