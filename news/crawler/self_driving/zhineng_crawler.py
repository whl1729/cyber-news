from typing import List

from bs4 import BeautifulSoup

from news.crawler import headers
from news.util import timelib
from news.util import web_crawler
from news.util.logger import logger
from news.util.web_parser import WebParser

ZHINENG_HOST = "https://xueqiu.com/u/zhineng"
XUEQIU_HOST = "https://xueqiu.com/"


class ZhinengParser(WebParser):
    def parse(self, resp_text: str) -> List[dict]:
        news_list = []
        soup = BeautifulSoup(resp_text, "lxml")
        for article in soup.find_all(class_="timeline__item"):
            article_time = article.find(class_="date-and-source")
            title = article.find(class_="timeline__item__content")
            news = {
                "id": title.h3.span.text,
                "url": XUEQIU_HOST + title.a["href"],
                "created_at": timelib.parse_time(article_time.text),
                "crawled_at": timelib.now2(),
            }
            news_list.append(news)
        logger.info(f"{len(news_list)} zhineng news parsed")
        return news_list


def crawl():
    parser = ZhinengParser()
    web_crawler.crawl(parser, ZHINENG_HOST, "zhineng", headers=headers)


if __name__ == "__main__":
    crawl()
