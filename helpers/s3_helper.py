"""This module contains a helper for the crawling process.

Compare a local file with the latest S3 resource, and
upload the difference to S3.
These links are jobs pages that will be scraped by the
module `wttj.py` and inserted in the database.
"""

import re
import ast
from typing import Set

import boto3
import datetime
from pathlib import Path
import logging

from config.definitions import PROJECT_PATH


class S3Helper:
    """This class helps to upload new links only.

    Because the crawler gets all links from WTTJ website,
    and that some jobs are reposted with a different url,
    we want to avoid jobs to be scraped again.
    """

    def __init__(self):
        """Initializes the instance with S3 and today's information."""
        self.today = datetime.date.today()
        self.today_filename = f'wttj_links_{self.today}.txt'
        self.data_path = PROJECT_PATH / 'ingestion' / 'scrapy' / 'data'
        self.today_filepath = self.data_path / self.today_filename
        self.today_filepath_new = self.data_path / f'new_{self.today_filename}'
        self.s3 = boto3.resource('s3')
        self.bucket_name = 'crawler-job-links'

    def upload_new_links(self) -> Set:
        """Factory function to upload new links only.

        Returns:
            A set of uploaded links.
        """
        # Download the 2 files we wish to compare
        s3_links = self.extract_s3_links()
        local_links = self.extract_local_links(self.today_filepath)

        # Extract the constant part of the urls
        local_links_constant = self.extract_constant_url(local_links)
        s3_links_constant = self.extract_constant_url(s3_links)

        # Subtract links from S3 to links freshly scraped
        new_links = self.subtract_old_links(s3_links_constant, local_links_constant)

        # Write new links to a file and upload to S3
        self.write_new_links_to_file(new_links)
        
        # Upload to S3 without the 'new_' prefix
        self.s3.Bucket(self.bucket_name).upload_file(self.today_filepath_new, self.today_filename)

        return new_links

    def extract_s3_links(self) -> Set:
        """Extracts the latest S3 file's content.

        Returns:
            A set of urls.
        """
        filename = self.get_latest_s3_file()
        obj = self.s3.Object(self.bucket_name, key=filename)
        links = obj.get()['Body'].read().decode('utf-8')
        
        return ast.literal_eval(links)
    
    def get_latest_s3_file(self) -> str:
        """Get a bucket's latest modified file's name.

        Returns:
            A string of the file name.
        """
        bucket = self.s3.Bucket(self.bucket_name)
        last_modified_date = datetime.date(2022, 9, 1)  # A random old date
        latest_s3_file = None

        for s3_file in bucket.objects.all():
            s3_file_date = s3_file.last_modified.date()
            if last_modified_date < s3_file_date <= self.today:
                last_modified_date = s3_file_date
                latest_s3_file = s3_file

        return latest_s3_file.key

    @staticmethod
    def extract_local_links(filepath: str) -> Set:
        """Extracts today's local links.

        Will throw an error if the spider hasn't run today.

        Returns:
            A set of local links
        """
        with open(filepath, 'r') as f:
            links = f.read()
        return ast.literal_eval(links)

    @staticmethod
    def extract_constant_url(urls: set) -> Set:
        """Truncates the query part of the url.

        On welcometothejungle website, jobs get reposted
        with a different url, which makes them being scraped
        more than once.

        Returns:
            A set of truncated urls.
        """
        # Remove the query part that doesn't identify uniquely a job
        constant_urls = set()

        for url in urls:
            match = re.search(r'.*(?=\?q=)', url)
            if match:
                constant_urls.add(match.group(0))
            else:
                constant_urls.add(url)

        return constant_urls

    @staticmethod
    def subtract_old_links(s3_links: set, local_links: set) -> Set:
        """Subtracts from local (new) links, those that are already
        in S3 (old).

        Returns:
            A set of new links.
        """
        return local_links - s3_links

    def write_new_links_to_file(self, new_links: set) -> str:
        """Writes new links to local file.

        Overwrites it if it already exists.

        Returns:
            The written string.
        """
        new_links_str = str(new_links)

        with open(self.today_filepath_new, 'w+') as f:
            f.write(str(new_links))

        return new_links_str


if __name__ == '__main__':
    s3_helper = S3Helper()
    new_links = s3_helper.upload_new_links()
    print(f'There is {len(new_links)} new links')

