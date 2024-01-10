import scrapy
import re
import datetime

from scrapy.crawler import CrawlerProcess
from scrapy.loader import ItemLoader
from itemloaders.processors import Join

from helpers.s3_helper import S3Helper
from ingestion.scrapy.items import JobsCrawlerItem


class WttjSpider(scrapy.Spider):
    """
    Spider to scrape jobs information on Welcome to the Jungle Website.
    The individual pages are not rendered with Javascript and only uses Scrapy.
    """

    name = "wttj"

    def start_requests(self):
        s3_helper = S3Helper()
        new_links_filename = s3_helper.today_filepath_new
        new_links = s3_helper.extract_local_links(new_links_filename)
        for link in new_links:
            yield scrapy.Request(link, self.yield_job_item)

    def yield_job_item(self, response):
        l = ItemLoader(item=JobsCrawlerItem(), response=response)

        match = re.search(r'.*(?=\?q=)', response.url)  # url with random ending
        if match:
            l.add_value("url", match.group(0))
        else:
            l.add_value("url", response.url)

        l.add_value(
            "title",
            response.xpath(
                '//h2/text()'
            ).get(),
        )
        l.add_value(
            "company",
            response.xpath(
                '//h2/parent::div/div/a/div/span/text()'
            ).get(),
        )
        l.add_value(
            "location",
            response.xpath(
                '//h4/span[contains(text(),"Le lieu de travail")]/parent::h4/following-sibling::a//text()'
            ).get(),
        )
        l.add_value(
            "contract",
            response.xpath(
                '//i[@name="contract"]/following-sibling::text()'
            ).get(),
        )
        l.add_value(
            "industry",
            response.xpath(
                '//div[@data-testid="job-company-tag"]//text()'
            ).get(),
        )
        l.add_value(
            "text",
            response.xpath('//div[@data-testid="job-section-description"]/div//p/text()').getall(),
            Join(),
        )
        l.add_value(
            "remote",
            response.xpath(
                '//i[@name="remote"]/following-sibling::span/text()'
            ).get(),
        )
        l.add_value("created_at", datetime.date.today())

        yield l.load_item()


if __name__ == "__main__":
    process = CrawlerProcess(
        settings={
            "ROBOTSTXT_OBEY": False,
            "ITEM_PIPELINES": {
                "ingestion.scrapy.pipelines.JobsCrawlerPipeline": 300,
            },
            "AUTOTHROTTLE_ENABLED": True,
            "AUTOTHROTTLE_TARGET_CONCURRENCY": 1,
            "AUTOTHROTTLE_START_DELAY": 5,
            "AUTOTHROTTLE_MAX_DELAY": 60,
        }
    )
    process.crawl(WttjSpider)
    process.start()
