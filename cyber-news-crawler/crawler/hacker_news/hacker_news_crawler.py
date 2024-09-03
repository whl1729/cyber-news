from typing import List

from bs4 import BeautifulSoup
from bs4 import Tag
from crawler.util import mystr
from crawler.util import timelib
from crawler.util import web_crawler
from crawler.util.configer import config
from crawler.util.logger import logger
from crawler.util.web_parser import WebParser

hacker_news_url = "https://news.ycombinator.com/"


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

            news = {
                "id": athing["id"],
                "title": titleline.a.string,
                "url": titleline.a["href"],
                "host": self._get_host(titleline),
                "score": self._get_score(subtext),
                "comment_count": self._get_comment_count(subtext),
                "created_at": self._get_time(subtext),
                "updated_at": timelib.now2(),
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
            return timelib.now3()

        return age.get("title", timelib.now3())

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
        hacker_news_url,
        "hacker_news",
        proxies=config["proxies"],
    )


if __name__ == "__main__":
    crawl()
