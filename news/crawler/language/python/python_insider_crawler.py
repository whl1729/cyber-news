from typing import List

import feedparser

from news.util import timelib
from news.util import web_crawler
from news.util.configer import config
from news.util.logger import logger
from news.util.web_parser import WebParser

PYTHON_INSIDER_URL = "https://blog.python.org/feeds/posts/default?alt=rss"


class PythonInsiderParser(WebParser):
    def parse(self, resp_text: str) -> List[dict]:
        blog_list = []
        feed = feedparser.parse(resp_text)
        for entry in feed.entries:
            blog = {
                "id": entry.title,
                "url": entry.link,
                "created_at": timelib.format_time_2(entry.published),
                "crawled_at": timelib.now2(),
            }
            blog_list.append(blog)

        logger.info(f"{len(blog_list)} python insider blogs parsed")
        return blog_list


def crawl():
    parser = PythonInsiderParser()
    web_crawler.crawl(
        parser, PYTHON_INSIDER_URL, "python_insider", proxies=config["proxies"]
    )


if __name__ == "__main__":
    crawl()
