from typing import List

from bs4 import BeautifulSoup

from news.util import mystr
from news.util import timelib
from news.util import web_crawler
from news.util.configer import config
from news.util.logger import logger
from news.util.web_parser import WebParser

PYCODER_WEEKLY_URL = "https://pycoders.com/latest"
PYCODER_ISSUE_URL = "https://pycoders.com/issues/"


class PycoderWeeklyParser(WebParser):
    def parse(self, resp_text: str) -> List[dict]:
        soup = BeautifulSoup(resp_text, "lxml")
        title = soup.find(name="h1").text
        issue_no = mystr.extract_numbers(title)
        created_at = soup.body.find(name="p").text
        blogs = []

        for h2 in soup.find_all("h2"):
            if "Upcoming Python Events" in h2.text:
                break

            # 查找所有满足 `style` 的取值包含 `color: #3399CC` 的 `<a>` 元素
            for span in h2.find_next_siblings(
                "span", style=lambda v: v and "color: #3399CC" in v
            ):
                blog = {
                    "title": span.a.text,
                    "url": span.a["href"],
                }
                blogs.append(blog)

        logger.info(f"{len(blogs)} pycoder weekly blogs parsed")

        weekly = {
            "id": "Pycoder's Weekly " + title,
            "url": PYCODER_ISSUE_URL + issue_no,
            "blogs": blogs,
            "created_at": timelib.format_date_5(created_at),
            "crawled_at": timelib.now2(),
        }
        return [weekly]


def crawl():
    parser = PycoderWeeklyParser()
    web_crawler.crawl(
        parser, PYCODER_WEEKLY_URL, "pycoder_weekly", proxies=config["proxies"]
    )


if __name__ == "__main__":
    crawl()
