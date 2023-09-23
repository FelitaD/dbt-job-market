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
