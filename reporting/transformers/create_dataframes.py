import pandas as pd
import streamlit as st

from ..utils.run_query import run_query
from ..utils import companies_stmt, technos_stmt, all_jobs_stmt, relevant_jobs_stmt, sankey_stmt

companies_df = pd.DataFrame(run_query(companies_stmt))
technos_df = pd.DataFrame(run_query(technos_stmt))
all_jobs_df = pd.DataFrame(run_query(all_jobs_stmt))
relevant_df = pd.DataFrame(run_query(relevant_jobs_stmt))
sankey_df = pd.DataFrame(run_query(sankey_stmt))


def create_companies_st_df() -> st.data_editor:
    """Creates the companies dataframe in the UI.

    Returns:
        An instance of st.data_editor.
    """
    return st.data_editor(companies_df.sort_values(by=['company_name']),
                          use_container_width=True,
                          column_config={
                              "company_name": st.column_config.TextColumn('name (listing)'),
                              "name": st.column_config.TextColumn('name (glassdoor)'),
                              "url": st.column_config.LinkColumn('url', width='small'),
                              "industry": st.column_config.Column(),
                              "headquarters": st.column_config.Column(),
                              "rating": st.column_config.Column(),
                              "company_size": st.column_config.NumberColumn('size mean'),
                              "reviews_count": st.column_config.NumberColumn(),
                              "jobs_count": st.column_config.NumberColumn(),
                              "salaries_count": st.column_config.NumberColumn(),
                          })


def create_technos_st_df(key) -> st.data_editor:
    """Creates the technologies dataframe in the UI.

    Returns:
        An instance of st.data_editor.
    """
    return st.data_editor(technos_df,
                          use_container_width=True,
                          column_order=('total', 'techno', 'category', 'subcategory', 'description'),
                          column_config={
                              'total': st.column_config.Column(width='small', label='total'),
                              'techno': st.column_config.Column(label='techno name'),
                              'category': st.column_config.Column(),
                              'subcategory': st.column_config.Column(),
                              'description': st.column_config.Column(),
                          },
                          key=key)


def create_relevant_jobs_st_df(df: pd.DataFrame) -> st.dataframe:
    """Creates the job board dataframe in the UI.

    Args:
        df: A filtered or unfiltered dataframe.

    Returns:
        An instance of st.data_editor.
    """
    return st.dataframe(
        df.style
        # .apply(highlight_total_score, axis=1)
        .format('{:.0f}', subset=['total_score', 'company_size', 'reviews_count', 'jobs_count', 'salaries_count'])
        .format('{:.1f}', subset=['rating']),
        use_container_width=True,
        column_order=(
            # 'rating_score',
            # 'seniority_score',
            'url_1',
            'url',
            'company',
            'title',
            'stack',
            'contract',
            'remote',
            'location',
            # 'text',
            'rating',
            'total_score',
            'is_same_glassdoor',
            'headquarters',
            'industry',
            'company_size',
            'reviews_count',
            'jobs_count',
            'salaries_count',
            'created_at',
            'id',
            # 'industry_1',
            # 'company_name',
            # 'name',
            # 'id_1',
            # 'is_relevant_score',
        ),
        column_config={
            'total_score': st.column_config.Column(width='small', label='🏆score'),
            # 'seniority_score': st.column_config.Column(width='small'),
            # 'rating_score': st.column_config.Column(width='small', label='📊rating score'),
            'title': st.column_config.Column(width='medium', label='👩‍💻title'),
            'company': st.column_config.Column(width='small', label='💼company'),
            'stack': st.column_config.ListColumn(width='large', label='🛠️stack'),
            'text': st.column_config.Column(width='medium', label='📝job description'),
            'url_1': st.column_config.LinkColumn(width='small', label='🔗url'),
            'contract': st.column_config.Column(width='small', label='📜contract'),
            'created_at': st.column_config.DateColumn(width='small', label='📅created at'),
            'industry': st.column_config.Column(width='medium', label='🏭industry'),
            'remote': st.column_config.Column(width='small', label='🏠remote'),
            'location': st.column_config.Column(width='medium', label='🌍location'),
            'headquarters': st.column_config.Column(width='medium', label='🌍headquarters'),
            'url': st.column_config.LinkColumn(width='small', label='🔗url (glassdoor)'),
            'is_same_glassdoor': st.column_config.Column(width='small', label='is same glassdoor'),
            'rating': st.column_config.Column(width='small', label='⭐️rating'),
            'company_size': st.column_config.Column(width='small', label='👥size'),
            'reviews_count': st.column_config.Column(width='small', label='📊reviews count'),
            'jobs_count': st.column_config.Column(width='small', label='📊jobs count'),
            'salaries_count': st.column_config.Column(width='small', label='📊salaries count'),
            'id': st.column_config.Column(width='small'),
            # 'industry_1': st.column_config.Column(width='medium'),
            # 'company_name': st.column_config.Column(width='medium'),
            # 'name': st.column_config.Column(width='medium'),
            # 'id_1': st.column_config.Column(width='small'),
            # 'is_relevant': st.column_config.Column(width='small'),
        },
        height=600
    )
