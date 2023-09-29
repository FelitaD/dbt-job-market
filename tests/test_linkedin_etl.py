import pytest
import pandas as pd
import numpy as np
import datetime
from pandas import DataFrame
from pandas.testing import assert_frame_equal

from ingestion.octoparse.linkedin_etl import LinkedinETL


class TestLinkedinETL:
    def test_extract_latest_crawl_type(self, etl):
        df = etl.extract_latest_crawl()
        assert isinstance(df, DataFrame)

    def test_transform_generic(self, etl, raw, transformed_generic):
        expected_transformed_generic = transformed_generic
        actual_transformed_generic = etl.transform_generic(raw)
        assert_frame_equal(expected_transformed_generic, actual_transformed_generic)
        
    def test_transform_date_posted(self, etl, transformed_generic_date, transformed_date):
        expected_transformed_date = transformed_date
        actual_transformed_date = etl.transform_date_posted(transformed_generic_date)
        assert_frame_equal(expected_transformed_date, actual_transformed_date)

    def test_parse_created_at(self, etl):
        today = datetime.date.today()
        actual = etl.parse_created_at('1 week ago')
        expected = today - datetime.timedelta(weeks=1)
        assert actual == expected
