"""Produces all jobs (not relevant included) dataframe in Streamlit.

Data stems from the same query as `job_board.py` but without
the `relevant = 1` condition. Hence it doesn't create another st.editor.
"""

import pandas as pd
import streamlit as st

from reporting.helpers.run_query import run_query
from config.definitions import all_jobs_stmt

all_jobs_df = pd.DataFrame(run_query(all_jobs_stmt))