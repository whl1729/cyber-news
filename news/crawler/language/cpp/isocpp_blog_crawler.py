from typing import List
from typing import Tuple

from bs4 import BeautifulSoup

from news.util import timelib
from news.util import web_crawler
from news.util.configer import config
from news.util.logger import logger
from news.util.web_parser import WebParser

ISOCPP_BLOG_URL = "https://isocpp.org/blog"


class IsocppBlogParser(WebParser):
    def parse(self, resp_text: str) -> List[dict]:
        soup = BeautifulSoup(resp_text, "lxml")
        blog_list = []
        for article in soup.find_all(name="article"):
            a = article.find(name="a")
            title, author = self._extract_title_and_author(a.string)
            byline = article.find(class_="byline")
            created_at = self._extract_time(byline.text)
            blog = {
                "id": title,
                "url": a["href"],
                "author": author,
                "created_at": created_at,
                "crawled_at": timelib.now2(),
            }
            blog_list.append(blog)
        logger.info(f"{len(blog_list)} isocpp blogs parsed")
        return blog_list

    @staticmethod
    def _extract_title_and_author(headline: str) -> Tuple[str, str]:
        """
        :param headline: 待解析的标题。示例："CppCon 2024 When Nanoseconds Matter: Ultrafast Trading Systems in C++ -- David Gross"
        """
        parts = headline.split("--")
        if len(parts) >= 2:
            title = "".join(parts[:-1]).strip()
            return title, parts[-1].strip()
        return headline.strip(), "Blog Stuff"

    @staticmethod
    def _extract_time(byline: str) -> str:
        """
        :param byline: 待解析的小行。示例："By Blog Staff \n| Sep 2, 2024 02:13 PM \n| Tag"
        """
        parts = byline.split("|")
        return timelib.format_time(parts[1].strip())


def crawl():
    parser = IsocppBlogParser()
    web_crawler.crawl(parser, ISOCPP_BLOG_URL, "isocpp_blog", proxies=config["proxies"])


if __name__ == "__main__":
    crawl()
