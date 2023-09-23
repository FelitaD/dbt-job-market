import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from google.oauth2 import service_account
from google.cloud import bigquery

from helpers.queries import sankey_stmt

credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = bigquery.Client(credentials=credentials)

tab_welcome, tab_doc, tab_about_me = st.tabs(['Welcome', 'Documentation', 'About me'])


@st.cache_data(ttl=600)
def run_query(query):
    query_job = client.query(query)
    rows_raw = query_job.result()
    # Convert to list of dicts. Required for st.cache_data to hash the return value.
    rows = [dict(row) for row in rows_raw]
    return rows


## Sankey diagram

with tab_welcome:
    sankey_df = pd.DataFrame(run_query(sankey_stmt))
    data = {
        'raw': {
            'pos': sankey_df.jobs,
            'neg': sankey_df.raw - sankey_df.jobs
        },
        'jobs': {
            'pos': sankey_df.relevant,
            'neg': sankey_df.jobs - sankey_df.relevant
        },
        'relevant': {
            'senior': sankey_df.senior,
            'junior': sankey_df.junior,
            'graduate': sankey_df.graduate,
            'unspecified': sankey_df.unspecified
        }
    }
    fig = go.Figure(data=[go.Sankey(
        arrangement='snap',
        node=dict(
            label=[
                'raw',  # 0
                'jobs',  # 1
                '',  # 2
                'relevant',  # 3
                '',  # 4
                'senior',  # 5
                'junior',  # 6
                'graduate',  # 7
                'unspecified',  # 8
            ],
            color='blue',
            x=[0, .25, .25, .5, .5, 1, 1, 1, 1],
            y=[.1, .1, .1, .1, .1, .4, .6, .5, .3]

        ),
        link=dict(
            source=[0, 0, 1, 1, 3, 3, 3, 3],
            target=[1, 2, 3, 4, 5, 6, 7, 8],
            value=[
                data['raw']['pos'][0],
                data['raw']['neg'][0],
                data['jobs']['pos'][0],
                data['jobs']['neg'][0],
                data['relevant']['senior'][0],
                data['relevant']['junior'][0],
                data['relevant']['graduate'][0],
                data['relevant']['unspecified'][0],
            ],
            color=['red', 'gray', 'red', 'gray', 'red', 'red', 'red', 'red']
        ),

    )])
    st.plotly_chart(fig)

with tab_doc:
    st.markdown(
        """
        # Job Radar 2.0
    
        Version 2 of [Job Radar 1.0](https://github.com/FelitaD/job-radar-1.0) by modifying technologies used.
        
        Focus is emphasized on analytics engineering using [Snowflake](https://www.snowflake.com/en/) coupled with [dbt](https://www.getdbt.com/) 
        and visualisations in Looker Studio and Streamlit. Orchestration with Prefect. Data modeling with Data Vault.
    
        """
    )
    # st.components.v1.html(
    #     """
    #     <iframe width="968" height="632" src="https://miro.com/app/live-embed/uXjVMNceW10=/?moveToViewport=-492,5651,4500,1505&embedId=45852963792" frameborder="0" scrolling="no" allow="fullscreen; clipboard-read; clipboard-write" allowfullscreen></iframe>
    #     """,
    #     width=1000,
    #     height=600
    # )
    # st.components.v1.html(
    #     """
    #     <iframe width="560" height="315" src='https://dbdiagram.io/embed/65083b9d02bd1c4a5ec730d7'> </iframe>
    #     """,
    #     width=1000,
    #     height=600
    # )

# from reporting.helpers.queries import all_data_stmt
#
# all_data = pd.DataFrame(run_query(all_data_stmt))
# all_data.to_csv('transformation/analyses/all_data.csv')
