from typing import List

import feedparser

from news.util import timelib
from news.util import web_crawler
from news.util.configer import config
from news.util.logger import logger
from news.util.web_parser import WebParser

INFOQ_URL = "https://feed.infoq.com/"


class InfoQParser(WebParser):
    def parse(self, resp_text: str) -> List[dict]:
        blog_list = []
        feed = feedparser.parse(resp_text)
        for entry in feed.entries:
            blog = {
                "id": entry.title,
                "url": entry.link,
                "author": entry.author,
                "created_at": timelib.format_iso_time(entry.updated),
                "crawled_at": timelib.now2(),
            }
            blog_list.append(blog)

        logger.info(f"{len(blog_list)} infoq blogs parsed")
        return blog_list


def crawl():
    parser = InfoQParser()
    web_crawler.crawl(parser, INFOQ_URL, "infoq", proxies=config["proxies"])


if __name__ == "__main__":
    crawl()
