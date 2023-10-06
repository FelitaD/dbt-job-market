import streamlit as st

st.set_page_config(
    page_title="Job Radar",
    page_icon="🎯",
    layout="wide",
)

from streamlit import session_state as state
from streamlit_timeline import timeline
from streamlit_elements import elements, sync, event
from types import SimpleNamespace

from reporting.dashboard import Dashboard, Treemap, Sankey, Scatter, RadialBar
from reporting.transformers import create_relevant_jobs_st_df, DataframeFilter


def main():
    tab_dashboard, tab_job_board, tab_timeline = st.tabs(['Dashboard', 'Job Board', 'Resume Timeline'])

    with st.sidebar:
        st.markdown("<h1 style='text-align: center'>Job Radar</h1>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:90%; text-align: center'>Search and compare data engineer positions</p>",
                    unsafe_allow_html=True)
        st.markdown("<p align='center'><a href='https://github.com/FelitaD/job-radar-2.0'><img "
                    "src='https://img.shields.io/badge/View_on_Github-000000?logo=github'></a></p>",
                    unsafe_allow_html=True)

        add_filters = st.checkbox('Add Job Board filters')
        df_filter = DataframeFilter()

        if add_filters:
            # Slider widgets
            start_rating, end_rating = df_filter.create_slider('rating')
            start_reviews_count, end_reviews_count = df_filter.create_slider('reviews_count')
            start_company_size, end_company_size = df_filter.create_slider('company_size')
            start_total_score, end_total_score = df_filter.create_slider('total_score')
            # Multiselect widgets
            created_at_filter = df_filter.create_multiselect('created_at')
            industry_filter = df_filter.create_multiselect('industry')
            stack_filter = df_filter.create_multiselect('stack')
            remote_filter = df_filter.create_multiselect('remote')

            # Create a filtered dataframe using widget default / user inputs
            filtered_df = df_filter.filter_dataframe(
                fields=['rating', 'reviews_count', 'company_size', 'total_score',
                        'created_at', 'industry', 'stack', 'remote'],
                start_rating=start_rating,
                end_rating=end_rating,
                start_reviews_count=start_reviews_count,
                end_reviews_count=end_reviews_count,
                start_company_size=start_company_size,
                end_company_size=end_company_size,
                start_total_score=start_total_score,
                end_total_score=end_total_score,
                created_at_filter=created_at_filter,
                industry_filter=industry_filter,
                stack_filter=stack_filter,
                remote_filter=remote_filter)

    with tab_job_board:
        if add_filters:
            st.write(f'{len(filtered_df)} jobs')
            create_relevant_jobs_st_df(filtered_df)  # Filtered dataframe
        else:
            st.write(f'{len(df_filter.df)} jobs')
            create_relevant_jobs_st_df(df_filter.df)  # Unfiltered dataframe
        """
        - _is_same_glassdoor_: Indicates if the company name collected on Glassdoor is the same as in the job posting.
        If 0, manual verification is recommended.
        - _company_size_: The mean of the original data of the form '1 to 50 employees'.
        """

    with tab_dashboard:
        if "w" not in state:
            board = Dashboard()
            w = SimpleNamespace(
                dashboard=board,
                radial=RadialBar(board, 0, 0, 6, 6, minW=3, minH=4),
                scatter=Scatter(board, 0, 0, 6, 6, minW=3, minH=4),
                treemap=Treemap(board, 0, 6, 6, 6, minW=3, minH=3),
                sankey=Sankey(board, 0, 0, 6, 6, minW=3, minH=4),
            )
            state.w = w
        else:
            w = state.w

        with elements("demo"):
            event.Hotkey("ctrl+s", sync(), bindInputs=True, overrideDefault=True)

            with w.dashboard(rowHeight=57):
                w.radial()
                w.treemap()
                w.sankey()
                w.scatter()

    with tab_timeline:
        with open('docs/timeline.json', "r") as f:
            data = f.read()

        # TODO: make the years appear completely at the bottom
        timeline(data, height=800)
        """
        Events are categorized as _academic_, _work_ and _certificates_ for easier navigation.
        My [Github Portfolio](https://github.com/FelitaD/Portfolio) contains projects and other online courses.
        """


if __name__ == "__main__":
    main()
