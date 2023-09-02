# streamlit_app.py

import streamlit as st

# Initialize connection.
conn = st.experimental_connection('snowflake', type='sql')

# Perform query.
df = conn.query('SELECT * from int_job_postings_technos;', ttl=600)

# Print results.
for row in df.itertuples():
    st.write(f"Job id {row.id} titled {row.title}:")