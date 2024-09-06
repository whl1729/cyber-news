from typing import List

from bs4 import BeautifulSoup

from news.crawler import headers
from news.util import timelib
from news.util import web_crawler
from news.util.logger import logger
from news.util.web_parser import WebParser

LIANGZIWEI_URL = "https://www.qbitai.com/"


class LiangziweiParser(WebParser):
    def parse(self, resp_text: str) -> List[dict]:
        news_list = []
        soup = BeautifulSoup(resp_text, "lxml")
        article_list = soup.find(class_="article_list")
        for article in article_list.find_all(class_="picture_text"):
            text_box = article.find(class_="text_box")
            news = {
                "id": text_box.h4.a.string,
                "url": text_box.h4.a["href"],
                "author": text_box.div.span.string,
                "created_at": timelib.parse_time(
                    text_box.div.find(class_="time").string
                ),
                "crawled_at": timelib.now2(),
            }
            news_list.append(news)
        logger.info(f"{len(news_list)} liangziwei news parsed")
        return news_list


def crawl():
    parser = LiangziweiParser()
    web_crawler.crawl(parser, LIANGZIWEI_URL, "liangziwei", headers=headers)


if __name__ == "__main__":
    crawl()
