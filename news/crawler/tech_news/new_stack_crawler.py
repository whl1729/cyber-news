from typing import List

import feedparser

from news.util import timelib
from news.util import web_crawler
from news.util.configer import config
from news.util.logger import logger
from news.util.web_parser import WebParser

NEW_STACK_URL = "https://thenewstack.io/blog/feed/"


class NewStackParser(WebParser):
    def parse(self, resp_text: str) -> List[dict]:
        blog_list = []
        feed = feedparser.parse(resp_text)
        for entry in feed.entries:
            blog = {
                "id": entry.title,
                "url": entry.link,
                "author": entry.author,
                "created_at": timelib.format_time_2(entry.published),
                "crawled_at": timelib.now2(),
            }
            blog_list.append(blog)

        logger.info(f"{len(blog_list)} new stack blogs parsed")
        return blog_list


def crawl():
    parser = NewStackParser()
    web_crawler.crawl(parser, NEW_STACK_URL, "new_stack", proxies=config["proxies"])


if __name__ == "__main__":
    crawl()
