import pandas as pd
import plotly.express as px

from reporting.dataframes.technos_df import technos_df

treemap_technos = px.treemap(technos_df,
                             path=['category', 'subcategory', 'techno'],
                             values='total',
                             hover_data={
                                 'category': False,
                                 'subcategory': False,
                                 'techno': False,
                                 'description': False},
                             height=800,
                             color='category',
                             color_discrete_sequence=px.colors.qualitative.Pastel
                             )
