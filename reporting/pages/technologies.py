import streamlit as st

from helpers.filter_dataframe import filter_dataframe


st.set_page_config(page_title="Data engineering job radar", page_icon="⛅︎", layout="wide")

st.write('Technologies occurences in job postings. The categorisation is taken from https://mad.firstmark.com/')

conn = st.experimental_connection('snowflake', type='sql')

techno_occurences = conn.query('SELECT * from techno_occurences;', ttl=600)
techno_occurences_copy = techno_occurences.copy()

jobs = conn.query('select * from int_job_postings_technos;')
jobs_copy = jobs

st.dataframe(filter_dataframe(techno_occurences_copy))



