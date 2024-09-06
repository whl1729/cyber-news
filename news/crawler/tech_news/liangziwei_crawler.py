from typing import List

from bs4 import BeautifulSoup

from news.crawler import headers
from news.util import mystr
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
                "created_at": self._parse_time(text_box.div.find(class_="time").string),
                "crawled_at": timelib.now2(),
            }
            news_list.append(news)
        logger.info(f"{len(news_list)} liangziwei news parsed")
        return news_list

    @staticmethod
    def _parse_time(time_str: str) -> str:
        if "分钟前" in time_str:
            minutes = mystr.extract_leading_numbers(time_str)
            return timelib.n_minutes_ago(minutes)

        if "小时前" in time_str:
            hours = mystr.extract_leading_numbers(time_str)
            return timelib.n_hours_ago(hours)

        if "昨天" in time_str:
            return time_str.replace("昨天", timelib.yesterday())

        if "前天" in time_str:
            return time_str.replace("前天", timelib.n_days_ago(2))

        return time_str


def crawl():
    parser = LiangziweiParser()
    web_crawler.crawl(parser, LIANGZIWEI_URL, "liangziwei", headers=headers)


if __name__ == "__main__":
    crawl()
