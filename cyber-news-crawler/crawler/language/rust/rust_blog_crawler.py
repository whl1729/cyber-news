from typing import List

from bs4 import BeautifulSoup
from crawler.util import timelib
from crawler.util import web_crawler
from crawler.util.configer import config
from crawler.util.web_parser import WebParser

RUST_BLOG_URL = "https://blog.rust-lang.org/"


class RustBlogParser(WebParser):
    def parse(self, resp_text: str) -> List[dict]:
        soup = BeautifulSoup(resp_text, "lxml")
        table = soup.find(name="table")
        blog_list = []
        for tr in table.select("tr"):
            td2 = tr.td.find_next_sibling(name="td")
            if tr.td.string is None:
                year = self._parse_year(td2.text)
                continue

            blog = {
                "id": td2.a.string,
                "url": RUST_BLOG_URL + td2.a["href"],
                "created_at": self._parse_date(tr.td.string, year),
                "crawled_at": timelib.now2(),
            }
            blog_list.append(blog)
        return blog_list

    @staticmethod
    def _parse_year(headline: str) -> str:
        """
        :param headline: 标题。示例："Posts in 2024"
        """
        return headline.removeprefix("Posts in ").strip()

    @staticmethod
    def _parse_date(date_str: str, year: str) -> str:
        """
        :param date_str: 日期字符串。示例："Aug.&nbsp;26"
        :param year: 年份。示例："2024"
        """
        formatted_str = (
            date_str.replace("\xa0", " ").replace(".", "").replace("Sept", "Sep")
        )
        return timelib.format_date_2(f"{formatted_str} {year}")


def crawl():
    parser = RustBlogParser()
    web_crawler.crawl(parser, RUST_BLOG_URL, "rust_blog", proxies=config["proxies"])


if __name__ == "__main__":
    crawl()
