"""This module contains functions used for Pandas' `apply`.

These functions might be used in the `job_board.py` module.
"""

import pandas as pd

from pandas import DataFrame, Series
from typing import List


def create_color(type: str, decrease_step: float) -> str:
    """Creates a rgba color.

    Args:
        type:
            If color should represent a good, bad or
            neutral feature.
        decrease_step:
            Of how much the opacity should be decreased.

    Returns:
        A string representing color. For example:
        rgba(24, 101, 98, 0.8)
    """
    good = tuple([24, 101, 98])
    bad = tuple([148, 94, 25])
    neutral = tuple([230, 232, 214])

    if type == 'good':
        return f'rgba{good + tuple([1 - decrease_step])}'
    if type == 'bad':
        return f'rgba{bad + tuple([1 - decrease_step])}'
    if type == 'neutral':
        return f'rgba{neutral + tuple([1 - decrease_step])}'


def highlight_total_score(df: DataFrame) -> List:
    """Highlight the rows with colors based on total_score column.

    The total_score column is calculated based on the seniority
    score and the companies' rating_score. 
    
    Args:
        df: The dataframe to apply styling to.

    Returns:
        A list of CSS expression strings.
    """
    score = df['total_score']
    if score == 6:
        return [f'background-color: {create_color("good", 0)}'] * len(df)
    elif score == 5:
        return [f'background-color: {create_color("good", 0.2)}'] * len(df)
    elif score == 4:
        return [f'background-color: {create_color("good", 0.4)}'] * len(df)
    elif score == 3:
        return [f'background-color: {create_color("good", 0.6)}'] * len(df)
    elif score == 2:
        return [f'background-color: {create_color("good", 0.8)}'] * len(df)
    elif score == 1:
        return [f'background-color: {create_color("neutral", 0.6)}'] * len(df)
    elif score == 0:
        return [f'background-color: {create_color("bad", 0.8)}'] * len(df)
    elif score == -1:
        return [f'background-color: {create_color("bad", 0.6)}'] * len(df)
    elif score == -2:
        return [f'background-color: {create_color("bad", 0.4)}'] * len(df)
    elif score == -3:
        return [f'background-color: {create_color("bad", 0.2)}'] * len(df)
    elif score == -4:
        return [f'background-color: {create_color("bad", 0)}'] * len(df)
    else:
        return [''] * len(df)


def highlight_quant_column(series: Series) -> List:
    """Highlight a single quantitative column.

    The colors are calculated based on how the value compares
    to the median.

    Args:
        series: A series containing numeric values.

    Returns:
        A list of CSS expression strings.
    """
    median = series.median()
    return [f'background-color: {create_color("good", 0)}' if v > median
            else f'background-color: {create_color("neutral", 0)}'
            if median - 0.1 < v < median + 0.1 or v == 0 or pd.isna(v)
            else f'background-color: {create_color("bad", 0)}' for v in series]
