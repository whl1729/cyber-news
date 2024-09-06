from typing import List

from bs4 import BeautifulSoup

from news.crawler import headers
from news.util import timelib
from news.util import web_crawler
from news.util.logger import logger
from news.util.web_parser import WebParser

GEEKPARK_HOST = "https://www.geekpark.net"


class GeekparkParser(WebParser):
    def parse(self, resp_text: str) -> List[dict]:
        news_list = []
        soup = BeautifulSoup(resp_text, "lxml")
        article_list = soup.find(class_="article-list")
        for article in article_list.find_all(class_="article-item"):
            article_time = article.find(class_="article-time")
            title = article.find(
                "a", attrs={"data-event-category": "article-list.title"}
            )
            news = {
                "id": title.h3.text,
                "url": GEEKPARK_HOST + title["href"],
                "created_at": timelib.parse_time(article_time.text),
                "crawled_at": timelib.now2(),
            }
            news_list.append(news)
        logger.info(f"{len(news_list)} geekpark news parsed")
        return news_list


def crawl():
    parser = GeekparkParser()
    web_crawler.crawl(parser, GEEKPARK_HOST, "geekpark", headers=headers)


if __name__ == "__main__":
    crawl()
