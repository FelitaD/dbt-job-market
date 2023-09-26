"""Produces a treemap of technologies using plotly.

Represents technologies frequency where each technology
can appear once at most in each job posting.
The categories and subcategories are extracted from
the MAD 2023.
"""
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
