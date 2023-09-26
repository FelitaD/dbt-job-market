"""Produces a scatter plot using Plotly.

Represent the distribution of companies' ratings on Glassdoor
compared to the number of reviews.
The graph also adds the percentiles as box plots on the margins.
The size of a company is represented by the size of the marker.
"""

import plotly.express as px

from reporting.dataframes.companies_df import companies_df

scatter_companies = px.scatter(companies_df[companies_df.company_size.notnull()],
                               x="reviews_count",
                               y="rating",
                               size='company_size',
                               log_x=True,
                               height=600,
                               template='plotly_dark',
                               color='company_size',
                               color_continuous_scale=px.colors.diverging.BrBG,
                               marginal_x="box",
                               marginal_y="box",
                               )
