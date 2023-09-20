import streamlit as st
import altair as alt
import pandas as pd

from reporting.home import client, run_query
from reporting.helpers.queries import all_companies_stmt

tab_data, tab_charts = st.tabs(['Data', 'Charts'])


with tab_data:
    companies = run_query(all_companies_stmt)
    companies_df = pd.DataFrame(companies)

with tab_charts:
    companies_chart = alt.Chart(companies_df).mark_circle().encode(
        x='reviews',
        y='rating',
    ).interactive()

    st.altair_chart(companies_chart)
    st.dataframe(companies)