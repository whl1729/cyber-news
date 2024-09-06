from typing import List

from bs4 import BeautifulSoup

from news.crawler import headers
from news.util import timelib
from news.util import web_crawler
from news.util.logger import logger
from news.util.web_parser import WebParser

JIQIZHIXIN_URL = "https://www.jiqizhixin.com"


class JiqizhixinParser(WebParser):
    def parse(self, resp_text: str) -> List[dict]:
        soup = BeautifulSoup(resp_text, "lxml")
        news_list = []
        for article in soup.find_all(name="article"):
            a = article.main.section.a
            news = {
                "id": a.string,
                "url": JIQIZHIXIN_URL + a["href"],
                "created_at": article.main.footer.div.span.time["datetime"].replace(
                    " +0800", ""
                ),
                "crawled_at": timelib.now2(),
            }
            news_list.append(news)
        logger.info(f"{len(news_list)} jiqizhixin news parsed")
        return news_list


def crawl():
    parser = JiqizhixinParser()
    web_crawler.crawl(parser, JIQIZHIXIN_URL, "jiqizhixin", headers=headers)


if __name__ == "__main__":
    crawl()
