import streamlit as st

from helpers.filter_dataframe import filter_dataframe


st.set_page_config(page_title="Data engineering job radar", page_icon="⛅︎", layout="wide")


conn = st.experimental_connection('snowflake', type='sql')

stmt = """
select title, company, stack, rating, reviews, size, location, c.industry, c.url as glassdoor_url, j.url as job_url, text, created_at
from analytics.marts.jobs_technos_agg j
join analytics.marts.companies c
on j.company = c.name
and regexp_like(title, '.*(data|analytics).*(engineer|ingénieur).*|.*(engineer|ingénieur).*(data|données|big data|bigdata)', 'i')
order by rating desc;
"""
jobs = conn.query(stmt)
jobs_copy = jobs

st.dataframe(filter_dataframe(jobs))
jobs = conn.query('select * from int_job_postings_technos;')
jobs_copy = jobs

st.dataframe(filter_dataframe(jobs))
