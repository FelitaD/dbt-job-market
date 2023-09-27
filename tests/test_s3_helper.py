import pytest
import datetime

from helpers.s3_helper import S3Helper


class TestS3Helper:
    def __init__(self):
        self.s3_helper = S3Helper()

    def test_get_filename_today(self):
        today = datetime.date.today()
        assert self.s3_helper.get_filename_today() == today
