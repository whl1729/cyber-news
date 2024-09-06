from typing import List

from bs4 import BeautifulSoup

from news.crawler import headers
from news.util import timelib
from news.util import web_crawler
from news.util.logger import logger
from news.util.web_parser import WebParser

XINZHIYUAN_HOST = "https://36kr.com"
XINZHIYUAN_URL = "https://36kr.com/user/574825230"


class XinzhiyuanParser(WebParser):
    def parse(self, resp_text: str) -> List[dict]:
        news_list = []
        soup = BeautifulSoup(resp_text, "lxml")
        flow_list = soup.find(class_="author-detail-flow-list")
        for article in flow_list.find_all(class_="flow-item"):
            title = article.find(class_="article-item-title")
            time = article.find(class_="kr-flow-bar-time")
            news = {
                "id": title.string,
                "url": XINZHIYUAN_HOST + title["href"],
                "created_at": timelib.parse_time(time.text),
                "crawled_at": timelib.now2(),
            }
            news_list.append(news)
        logger.info(f"{len(news_list)} xinzhiyuan news parsed")
        return news_list


def crawl():
    parser = XinzhiyuanParser()
    web_crawler.crawl(parser, XINZHIYUAN_URL, "xinzhiyuan", headers=headers)


if __name__ == "__main__":
    crawl()
