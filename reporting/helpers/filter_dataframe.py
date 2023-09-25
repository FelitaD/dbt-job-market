import pandas as pd
import streamlit as st
import ast
import datetime

from pandas.api.types import is_list_like

from config.definitions import all_data_columns
from reporting.helpers.run_query import run_query
from reporting.helpers.queries import all_data_stmt


def create_unfiltered_df():
    df = pd.DataFrame(run_query(all_data_stmt))
    df['rating'] = df['rating'].astype(float)
    if not is_list_like(df['stack']):
        df['stack'] = df['stack'].apply(lambda x: ast.literal_eval(x))
    return df


def create_slider(field):
    df = create_unfiltered_df()
    s = df[df[field].notnull()][field].sort_values()
    _min = s.min()
    _max = s.max()
    field_name = field.replace('_', ' ').capitalize()
    return st.select_slider(
        label=f'{field_name}',
        options=s,
        value=(_min, _max),
        key=field
    )


def create_multiselect(field):
    df = create_unfiltered_df()
    field_name = field.replace('_', ' ').capitalize()
    if field == 'stack':
        s = df['stack'].explode().sort_values().unique()
    else:
        s = df[df[field].notnull()][field].sort_values(ascending=False).unique()
    return st.multiselect(
        label=f'{field_name}',
        options=s,
    )


def filter_dataframe(fields, **kwargs):
    bool_expr = []
    created_at_filter = kwargs.get('created_at_filter')
    industry_filter = kwargs.get('industry_filter')
    stack_filter = kwargs.get('stack_filter')

    for field in fields:
        start = kwargs.get(f'start_{field}')
        end = kwargs.get(f'end_{field}')
        if field in ['rating', 'reviews_count', 'company_size', 'total_score']:
            bool_expr += [f'{field} >= {start} & {field} <= {end}']
        elif field == 'created_at' and created_at_filter:
            bool_expr += [f"{field} == {created_at_filter}"]
        elif field == 'industry' and industry_filter:
            bool_expr += [f"{field} == {industry_filter}"]
        elif field == 'stack' and stack_filter:
            stack_filtered_df = df[df['stack'].apply(lambda x: all(keyword in x for keyword in stack_filter))]

    bool_expr_concat = ' & '.join(bool_expr)
    filtered_df = df.query(bool_expr_concat)

    if stack_filter:
        print('STACK')
        stack_filtered_df_x = stack_filtered_df.explode('stack')
        filtered_df_x = filtered_df.explode('stack')
        merged_df_x = stack_filtered_df_x.merge(filtered_df_x)

        keys = [column for column in all_data_columns if column != 'stack']
        merged_df = merged_df_x.groupby(by=keys, dropna=False).agg(list).reset_index()
        print('merged_df:', merged_df)

        print('merged_df:', merged_df[['id', 'stack']])
        return merged_df
    else:
        print('NOT STACK')
        return filtered_df
