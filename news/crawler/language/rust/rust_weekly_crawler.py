from typing import List
from typing import Tuple

from bs4 import BeautifulSoup

from news.util import timelib
from news.util import web_crawler
from news.util.configer import config
from news.util.logger import logger
from news.util.web_parser import WebParser

RUST_WEEKLY_INDEX_URL = "https://this-week-in-rust.org/"


class RustWeeklyParser(WebParser):
    def __init__(self, title: str, url: str):
        """
        :param title: 博客标题
        :param url: 博客 URL
        """
        self._title = title
        self._url = url

    def parse(self, resp_text: str) -> List[dict]:
        soup = BeautifulSoup(resp_text, "lxml")
        post_content = soup.find(class_="post-content")
        blogs = []
        for h3 in post_content.find_all(name="h3"):
            if h3["id"] == "rfcs":
                break
            ul = h3.find_next_sibling(name="ul")
            for li in ul.find_all(name="li"):
                if li.a is None:
                    continue

                blog = {
                    "title": li.a.text,
                    "url": li.a["href"],
                }
                blogs.append(blog)

        logger.info(f"{len(blogs)} rust weekly blogs parsed")
        published_time = soup.find(name="time")
        weekly = {
            "id": self._title,
            "url": self._url,
            "blogs": blogs,
            "created_at": timelib.format_date_4(published_time["datetime"]),
            "crawled_at": timelib.now2(),
        }
        return [weekly]


class RustWeeklyIndexParser:
    def parse(self, resp_text: str) -> Tuple[str, str]:
        soup = BeautifulSoup(resp_text, "lxml")
        a = soup.find(class_="row post-title").find(name="a")
        return a.text, a["href"]


def find_latest_issue() -> str:
    resp_text = web_crawler.get(
        url=RUST_WEEKLY_INDEX_URL,
        name="rust_weekly_index",
    )
    if resp_text == "":
        return ""

    parser = RustWeeklyIndexParser()
    return parser.parse(resp_text)


def crawl():
    title, url = find_latest_issue()
    parser = RustWeeklyParser(title, url)
    web_crawler.crawl(parser, url, "rust_weekly", proxies=config["proxies"])


if __name__ == "__main__":
    crawl()
