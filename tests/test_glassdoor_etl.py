import pytest
import pandas as pd
from pandas import DataFrame
from pandas.testing import assert_frame_equal

pd.set_option('display.width', 300)
pd.set_option('display.max_columns', 15)


class TestGlassdoorETL:

    def test_extract_latest_crawl_type(self, glassdoor_etl):
        glassdoor_etl.extract_latest_crawl()
        assert isinstance(glassdoor_etl.companies_data, DataFrame)

    def test_extract_company_names_type(self, glassdoor_etl):
        glassdoor_etl.extract_company_names()
        assert isinstance(glassdoor_etl.company_names, DataFrame)

    def test_concat_original_company_names_type(self, concatenated_company_names_urls):
        assert isinstance(concatenated_company_names_urls.data, DataFrame)

    def test_names_and_urls_match(self, concatenated_company_names_urls):
        """Doesn't test a function but rather the content of a DataFrame.

        Company names in the database and on Glassdoor might not be
        exactly the same. In order to test if they are matched correctly,
        we want to reach at least 40% resemblance.
        """
        data = concatenated_company_names_urls.data
        df = data[data['URL'].notna()]
        matches = df[['companies', 'URL']].apply(lambda x: True if x['companies'].lower() in x['URL'].lower() else False, axis=1)
        treshold = 40 * len(matches) / 100
        assert matches.sum() > treshold

    def test_transform(self, concatenated_company_names_urls, source_transformed_companies, expected_transformed_companies):
        concatenated_company_names_urls.data = source_transformed_companies
        concatenated_company_names_urls.transform()
        actual = concatenated_company_names_urls.data
        print(actual)
        print(expected_transformed_companies)
        assert_frame_equal(actual, expected_transformed_companies)