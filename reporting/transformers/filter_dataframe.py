"""This module contains the DataframeFilter class definition.

Main usages are in the `home.py` module.
"""
import pandas as pd
import streamlit as st
import ast
import datetime

from typing import List
from pandas import DataFrame
from pandas.api.types import is_list_like

from ..utils import run_query, all_data_columns, relevant_jobs_stmt


class DataframeFilter:
    """Creates all components needed to filter dataframe displayed in Streamlit.

    Longer class information...
    Longer class information...

    Attributes:
        df: The unfiltered dataframe used as base.
    """
    def __init__(self):
        """Initialises the instance.

        Creates an unfiltered dataframe on initialisation.
        """
        self.df = self.create_unfiltered_relevant_df()

    @staticmethod
    def create_unfiltered_relevant_df() -> DataFrame:
        """Creates a dataframe used by all filtering operations.

        The function requests the database indirectly via another function
        `run_query` that caches results for a given amount of time.
        Columns are then converted to needed data types for transformation.

        Returns:
            A Pandas DataFrame containing 3 tables joined together:
            jobs, companies and scores.
        """
        df = pd.DataFrame(run_query(relevant_jobs_stmt))
        df['rating'] = df['rating'].astype(float)

        if not is_list_like(df['stack']):
            df['stack'] = df['stack'].apply(lambda x: ast.literal_eval(x))

        return df

    def create_slider(self, field: str) -> List:
        """Creates a Streamlit widget `select_slider`.

        The slider has 2 selectors that can be moved in the UI to change
        minimum and maximum value of a given field.

        Args:
            field: The name of the column.

        Returns:
            A list of 2 numeric values. By default, the min and max value
            of the numeric column.
        """
        options = self.df[self.df[field].notnull()][field].sort_values()
        _min = options.min()
        _max = options.max()
        field_label = field.replace('_', ' ').capitalize()

        return st.select_slider(
            label=field_label,
            options=options,
            value=(_min, _max),
            key=field
        )

    def create_multiselect(self, field: str) -> List:
        """Creates a Streamlit widget `multiselect`.

        The multiselect allows to choose multiple values for a given field.

        Args:
            field: The name of the column.

        Returns:
            A list of values of the column's data type. Empty by default.
        """
        if field == 'stack':  # Which value is an array
            options = self.df['stack'].explode().sort_values().unique()
        else:
            options = self.df[self.df[field].notnull()][field].sort_values(ascending=False).unique()

        field_label = field.replace('_', ' ').capitalize()

        return st.multiselect(
            label=field_label,
            options=options,
        )

    def filter_dataframe(self, fields: List, **kwargs) -> DataFrame:
        """Filters the instance's base dataframe using widget default / user inputs.

        It creates a new filtered dataframe with boolean expressions of each field.
        If `stack_filter` is not empty, creates another dataframe that is merged
        to the previous one.

        Returns:
            A filtered dataframe.
        """
        # Initialize the boolean expression used as filter
        bool_expr = []

        # Get values of multiselect widgets (categorical fields)
        created_at_filter = kwargs.get('created_at_filter')
        industry_filter = kwargs.get('industry_filter')
        stack_filter = kwargs.get('stack_filter')
        remote_filter = kwargs.get('remote_filter')

        for field in fields:
            # Get start and end values of slider widgets (numeric fields)
            start = kwargs.get(f'start_{field}')
            end = kwargs.get(f'end_{field}')

            # Add boolean expression for each numeric and categorical fields
            if field in ['rating', 'reviews_count', 'company_size', 'total_score']:
                bool_expr += [f'( ({field} >= {start} & {field} <= {end}) | {field}.isnull() )']
            elif created_at_filter and field == 'created_at':
                bool_expr += [f"( {field} == {created_at_filter} | {field}.isnull() )"]
            elif industry_filter and field == 'industry':
                bool_expr += [f"( {field} == {industry_filter} | {field}.isnull() )"]
            elif remote_filter and field == 'remote':
                bool_expr += [f"( {field} == {remote_filter} | {field}.isnull() )"]

        # Create a string containing all boolean expressions
        bool_expr_concat = ' & '.join(bool_expr)

        # Create a filtered dataframe
        filtered_df = self.df.query(bool_expr_concat)

        if stack_filter:
            # Create a new dataframe since stack (array values) can't be filtered with a boolean expression
            stack_filtered_df = self.df[self.df['stack'].apply(
                lambda x: all(keyword in x for keyword in stack_filter)
            )]
            return self.merge_stack_df(filtered_df, stack_filtered_df)
        else:
            return filtered_df

    @staticmethod
    def merge_stack_df(filtered_df: DataFrame, stack_filtered_df: DataFrame) -> DataFrame:
        """Merges two dataframes where one column contains type list.

        Args:
            filtered_df: A filtered dataframe.
            stack_filtered_df: Another filtered dataframe.

        Returns:
            A dataframe.
        """
        # Explode the list column with one value per row
        stack_filtered_df_x = stack_filtered_df.explode('stack')
        filtered_df_x = filtered_df.explode('stack')
        # Merge the 2 dataframes
        merged_df_x = stack_filtered_df_x.merge(filtered_df_x)
        # Perform an aggregation that take the stack column back into a list
        keys = [column for column in all_data_columns if column != 'stack']
        merged_df = merged_df_x.groupby(by=keys, dropna=False).agg(list).reset_index()

        return merged_df
