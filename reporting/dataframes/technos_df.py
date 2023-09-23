import streamlit as st
import pandas as pd

from reporting.helpers.run_query import run_query
from reporting.helpers.queries import technos_stmt


technos_df = pd.DataFrame(run_query(technos_stmt))


def create_technos_st_df():

    technos_df_st = st.data_editor(technos_df,
                                   use_container_width=True,
                                   column_order=('total', 'techno', 'category', 'subcategory', 'description'),
                                   column_config={
                                       'total': st.column_config.Column(width='small', label='total'),
                                       'techno': st.column_config.Column(label='techno name'),
                                       'category': st.column_config.Column(),
                                       'subcategory': st.column_config.Column(),
                                       'description': st.column_config.Column(),
                                   })
    return technos_df_st
