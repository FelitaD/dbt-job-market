"""Produces a scatter plot using Plotly.

Represent the distribution of companies' ratings on Glassdoor
compared to the number of reviews.
The graph also adds the percentiles as box plots on the margins.
The size of a company is represented by the size of the marker.
"""

from ..transformers import companies_df


def transform_row(row):
    return {
        'id': row['name'],
        'data': [{'x': row['reviews_count'], 'y': row['rating'], 'z': row['company_size']}]
    }


def format_companies_stats():
    companies_stats = companies_df[['name', 'reviews_count', 'rating', 'company_size']]
    companies_stats['rating'] = companies_stats['rating'].astype(float)

    no_null_stats = companies_stats[companies_stats['rating'].notnull() & companies_stats['reviews_count'].notnull()]
    # companies_df = companies_df[(companies_df['rating'].notnull() & companies_df['reviews_count'].notnull())
    #                             & (companies_df['rating'] > 0 & companies_df['reviews_count'] > 0)]

    return no_null_stats.apply(transform_row, axis=1).tolist()


scatter_data = format_companies_stats()
