import streamlit as st
import altair as alt
import pandas as pd

from reporting.home import run_query
from reporting.helpers.queries import all_companies_stmt

tab_charts, tab_data = st.tabs(['Charts', 'Data'])


with tab_data:
    companies = run_query(all_companies_stmt)
    companies_df = pd.DataFrame(companies)

    st.dataframe(companies)

with tab_charts:

    companies_chart = alt.Chart(companies_df).mark_circle().encode(
        x='reviews',
        y='rating',
    ).interactive()

    st.altair_chart(companies_chart)
