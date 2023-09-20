import streamlit as st
import altair as alt
import pandas as pd

from reporting.home import client, run_query
from reporting.helpers.queries import techno_occurences_stmt

tab_data, tab_charts = st.tabs(['Data', 'Charts'])


with tab_data:

    techno_occurences = run_query(techno_occurences_stmt)
    chart_data = st.data_editor(techno_occurences)

with tab_charts:
    df = pd.DataFrame({
        'Technos': [row['techno'] for row in techno_occurences],
        'Counts': [row['total'] for row in techno_occurences]
    })
    source = df[df['Counts'] > 5].sort_values(by='Counts')
    print(source)

    c = alt.Chart(source).transform_joinaggregate(
        TotalCounts='sum(Counts)',
    ).transform_calculate(
        PercentOfTotal="datum.Counts / datum.TotalCounts"
    ).mark_bar().encode(
        alt.X('PercentOfTotal:Q').axis(format='.0%'),
        y='Technos:N'
    )

    st.altair_chart(c, use_container_width=True)