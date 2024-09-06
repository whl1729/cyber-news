from typing import List

from bs4 import BeautifulSoup

from news.util import timelib
from news.util import web_crawler
from news.util.configer import config
from news.util.logger import logger
from news.util.web_parser import WebParser

GO_WEEKLY_URL = "https://golangweekly.com/latest"


class GoWeeklyParser(WebParser):
    def parse(self, resp_text: str) -> List[dict]:
        soup = BeautifulSoup(resp_text, "lxml")
        title = soup.head.title.text
        created_at = title.split(":")[-1].strip()
        blogs = []
        for main_link in soup.find_all(class_="mainlink"):
            blog = {
                "title": main_link.a.text,
                "url": main_link.a["href"],
            }
            blogs.append(blog)

        logger.info(f"{len(blogs)} go weekly blogs parsed")

        weekly = {
            "id": title,
            "blogs": blogs,
            "created_at": timelib.format_date_3(created_at),
            "crawled_at": timelib.now2(),
        }
        return [weekly]


def crawl():
    parser = GoWeeklyParser()
    web_crawler.crawl(parser, GO_WEEKLY_URL, "go_weekly", proxies=config["proxies"])


if __name__ == "__main__":
    crawl()
