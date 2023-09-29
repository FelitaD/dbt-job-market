import pytest

from ingestion.octoparse.linkedin_etl import LinkedinETL


class TestLinkedinETL:

    @pytest.fixture()
    def etl(self):
        return LinkedinETL('linkedin_eu_remote')

    def test_extract_latest_crawl(self):
        pass