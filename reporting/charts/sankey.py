"""Produces a sankey diagram using Plotly and Pandas.

The purpose is to give a visual representation of how
many rows (i.e. job postings) remain at each stages
of the transformation in BigQuery.
"""

import pandas as pd
import plotly.graph_objects as go

from reporting.helpers.run_query import run_query
from config.definitions import sankey_stmt


# Create a copy of a Bigquery table as a Dataframe
sankey_df = pd.DataFrame(run_query(sankey_stmt))

# Create a dictionary that help identifying nodes
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

# Create the figure with plotly Sankey package
sankey_fig = go.Figure(data=[go.Sankey(
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
