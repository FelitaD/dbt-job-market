import pytest
import datetime
import boto3
import re

from helpers.s3_helper import S3Helper


class TestS3Helper:

    @pytest.fixture
    def s3_helper(self):
        return S3Helper()

    def test_get_latest_s3_file_type(self, s3_helper):
        latest_file = s3_helper.get_latest_s3_file()
        assert isinstance(latest_file, str)

    def test_get_latest_s3_file_extension(self, s3_helper):
        latest_file = s3_helper.get_latest_s3_file()
        assert latest_file.endswith('.txt')

    @pytest.fixture()
    def s3_links(self, s3_helper):
        return s3_helper.extract_s3_links()

    def test_extract_s3_links_type(self, s3_links):
        assert isinstance(s3_links, set)

    def test_extract_s3_links_url_regex(self, s3_links):
        matches = [re.match(r'https://www\.welcometothejungle\.com/.*', link) for link in list(s3_links)]
        for match in matches:
            assert match

    @pytest.fixture()
    def local_links(self, s3_helper):
        today_filepath = s3_helper.today_filepath
        return s3_helper.extract_local_links(today_filepath)

    def test_extract_local_links_type(self, local_links):
        assert isinstance(local_links, set)

    def test_extract_local_links_regex(self, local_links):
        matches = [re.match(r'https://www\.welcometothejungle\.com/.*', link) for link in list(local_links)]
        for match in matches:
            assert match

    def test_extract_constant_url_type(self, s3_helper, local_links):
        actual_constant_urls = s3_helper.extract_constant_url(local_links)
        assert isinstance(actual_constant_urls, set)

    def test_extract_constant_url(self, s3_helper):
        links = {'https://www.welcometothejungle.com/fr/companies/ornikar/jobs/data-engineer_paris_ORNIK_4Jq2W8W?q=b8d6cc177c4c9e65f20e5608837d1c25&o=1668315',
                 'https://www.welcometothejungle.com/fr/companies/decathlon-digital/jobs/senior-trainer-engineer-tableau-software-bi-tools-datavizualisation-f-m-d_croix?q=4c91c687bbdd18229b7b53247c921579&o=1783170'}
        expected_constant_urls = {'https://www.welcometothejungle.com/fr/companies/ornikar/jobs/data-engineer_paris_ORNIK_4Jq2W8W',
                                  'https://www.welcometothejungle.com/fr/companies/decathlon-digital/jobs/senior-trainer-engineer-tableau-software-bi-tools-datavizualisation-f-m-d_croix'}
        actual_constant_urls = s3_helper.extract_constant_url(links)
        assert expected_constant_urls == actual_constant_urls

    def test_extract_constant_url_query_missing(self, s3_helper):
        links = {'https://www.welcometothejungle.com/fr/companies/ornikar/jobs/data-engineer_paris_ORNIK_4Jq2W8W',
                                  'https://www.welcometothejungle.com/fr/companies/decathlon-digital/jobs/senior-trainer-engineer-tableau-software-bi-tools-datavizualisation-f-m-d_croix'}
        expected_constant_urls = {'https://www.welcometothejungle.com/fr/companies/ornikar/jobs/data-engineer_paris_ORNIK_4Jq2W8W',
                                  'https://www.welcometothejungle.com/fr/companies/decathlon-digital/jobs/senior-trainer-engineer-tableau-software-bi-tools-datavizualisation-f-m-d_croix'}
        actual_constant_urls = s3_helper.extract_constant_url(links)
        assert expected_constant_urls == actual_constant_urls

    def test_subtract_old_links(self, s3_helper):
        s3_links = {'dummy_url_1', 'dummy_url_2'}
        local_links = {'dummy_url_1', 'dummy_url_2', 'dummy_url_3', 'dummy_url_4'}
        expected_new_links = {'dummy_url_4', 'dummy_url_3'}
        actual_new_links = s3_helper.subtract_old_links(s3_links, local_links)
        assert actual_new_links == expected_new_links

    def test_write_new_links_to_file(self, s3_helper):
        dummy_links = {'dorian', 'gray'}
        new_links_str = s3_helper.write_new_links_to_file(dummy_links)
        assert new_links_str == "{'dorian', 'gray'}"


















