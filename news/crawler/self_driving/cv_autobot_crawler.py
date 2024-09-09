from typing import List

from bs4 import BeautifulSoup

from news.crawler import headers
from news.util import timelib
from news.util import web_crawler
from news.util.logger import logger
from news.util.web_parser import WebParser

CV_AUTOBOT_HOST = "https://blog.csdn.net/CV_Autobot"


class AutobotParser(WebParser):
    def parse(self, resp_text: str) -> List[dict]:
        news_list = []
        soup = BeautifulSoup(resp_text, "lxml")
        for article in soup.find_all(class_="blog-list-box"):
            title = article.find(name="h4")
            time = (
                article.find(class_="view-time-box")
                .text.split("\u00A0")[1]
                .strip()
                .replace(".", "-")
            )
            news = {
                "id": title.text.strip(),
                "url": article.a["href"],
                "created_at": timelib.parse_time(time),
                "crawled_at": timelib.now2(),
            }
            news_list.append(news)
        logger.info(f"{len(news_list)} cv_autobot news parsed")
        return news_list


def crawl():
    parser = AutobotParser()
    web_crawler.crawl(parser, CV_AUTOBOT_HOST, "cv_autobot", headers=headers)


if __name__ == "__main__":
    crawl()
