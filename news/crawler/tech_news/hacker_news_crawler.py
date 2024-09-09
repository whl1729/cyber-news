from typing import List

from bs4 import BeautifulSoup
from bs4 import Tag

from news.util import mystr
from news.util import timelib
from news.util import web_crawler
from news.util.configer import config
from news.util.logger import logger
from news.util.web_parser import WebParser

hacker_news_host = "https://news.ycombinator.com/"


class HackerNewsParser(WebParser):
    def parse(self, resp_text: str) -> List[dict]:
        news_list = []
        soup = BeautifulSoup(resp_text, "lxml")
        athing = soup.find(class_="athing")
        while athing:
            titleline = athing.find(class_="titleline")
            subtext = athing.next_sibling
            if not titleline.a:
                athing = subtext.find_next_sibling(class_="athing")
                continue

            url = titleline.a["href"]
            if "http" not in url:
                url = hacker_news_host + url

            news = {
                "id": titleline.a.string,
                "url": titleline.a["href"],
                "host": self._get_host(titleline),
                "score": self._get_score(subtext),
                "comment_count": self._get_comment_count(subtext),
                "created_at": self._get_time(subtext),
                "crawled_at": timelib.now2(),
            }
            news_list.append(news)

            athing = subtext.find_next_sibling(class_="athing")

        logger.info(f"{len(news_list)} hacker news parsed")
        return news_list

    @staticmethod
    def _get_host(titleline: Tag) -> str:
        try:
            return titleline.span.a.string
        except Exception as e:
            logger.error(
                f"Failed to get host for HackerNewsParser: {e}, Tag: {titleline}"
            )

    @staticmethod
    def _get_time(subtext: Tag) -> str:
        age = subtext.find(class_="age")
        if not age:
            return timelib.now2()

        try:
            return timelib.format_iso8601_time_2(age["title"])
        except ValueError as _:
            return timelib.now2()

    @staticmethod
    def _get_score(subtext: Tag) -> int:
        score = subtext.find(class_="score")
        if not score:
            return 0
        return mystr.extract_leading_numbers(score.string)

    @staticmethod
    def _get_comment_count(subtext: Tag) -> int:
        for anchor in reversed(subtext.span.find_all(name="a")):
            comment_str = anchor.string
            if "comments" in comment_str:
                return mystr.extract_leading_numbers(comment_str)
        return 0


def crawl():
    parser = HackerNewsParser()
    web_crawler.crawl(
        parser,
        hacker_news_host,
        "hacker_news",
        proxies=config["proxies"],
    )


if __name__ == "__main__":
    crawl()
