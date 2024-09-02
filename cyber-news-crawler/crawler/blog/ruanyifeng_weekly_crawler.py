import re
from typing import List
from typing import Optional
from typing import Tuple

from bs4 import BeautifulSoup
from bs4 import Tag
from crawler.util import web_crawler
from crawler.util.logger import logger
from crawler.util.web_parser import WebParser

ruanyifeng_blog_url = "https://www.ruanyifeng.com/blog/"


class RuanyifengWeeklyParser(WebParser):
    def __init__(self, title: str, url: str):
        """
        :param title: 博客标题
        :param url: 博客 URL
        """
        self._title = title
        self._url = url

    def parse(self, resp_text: str) -> List[dict]:
        soup = BeautifulSoup(resp_text, "lxml")
        blog = {
            "id": self._title,
            "url": self._url,
            "created_at": self._parse_date(soup),
            "sections": {
                "热点": self._parse_hot_news(soup),
            },
        }

        sections = ["科技动态", "文章", "工具", "AI 相关", "资源", "图片", "文摘"]
        for section in sections:
            blog["sections"][section] = self._parse_section(soup, section)
        return [blog]

    @staticmethod
    def _parse_date(soup: BeautifulSoup) -> str:
        for p in soup.find_all(name="p"):
            if "日期：" in p.text:
                return p.abbr["title"]

        # 为避免以上方案查不到，再查一下「发表日期」，双重保险
        for li in soup.find_all(name="li"):
            if "发表日期" in li.string:
                return li.abbr["title"]

        return ""

    @staticmethod
    def _parse_hot_news(soup: BeautifulSoup) -> List[str]:
        news_list = []
        id = 1
        for h2 in soup.find_all(name="h2"):
            if "封面图" in h2.string:
                continue
            if "科技动态" in h2.string:
                return news_list
            news_list.append(f"{id}. {h2.string}")
            id += 1

        return news_list

    def _parse_section(self, soup: BeautifulSoup, name_cn: str) -> List[str]:
        """
        :param name_cn: 章节的中文名字
        """
        news_list = []
        section = self._find_section(soup, name_cn)
        if section is None:
            return []

        # 查找以「数字+"、"」开头的段落，作为一条新闻的概括。比如："1、"
        pattern = r"\d+、"
        sibling = section.next_sibling
        while sibling.name != "h2":
            if re.search(pattern, sibling.text):
                news_list.append(sibling.text.replace("、", ". ", 1))
            sibling = sibling.next_sibling

        return news_list

    @staticmethod
    def _find_section(soup: BeautifulSoup, name_cn: str) -> Optional[Tag]:
        for h2 in soup.find_all(name="h2"):
            if name_cn in h2.string:
                return h2
        return None


class RuanyifengBlogParser:
    def parse(self, resp_text: str) -> Tuple[str, str]:
        soup = BeautifulSoup(resp_text, "lxml")
        a = soup.h2.a
        return a.string, a["href"]


def find_latest_blog() -> str:
    resp_text = web_crawler.get(
        url=ruanyifeng_blog_url,
        name="ruanyifeng_blog",
    )
    if resp_text == "":
        return ""

    parser = RuanyifengBlogParser()
    return parser.parse(resp_text)


def crawl():
    title, url = find_latest_blog()
    if title == "" or url == "":
        logger.error(f"Failed to find yuanyifeng latest blog: title={title}, url={url}")
        return

    parser = RuanyifengWeeklyParser(title, url)
    web_crawler.crawl(
        parser,
        url,
        "ruanyifeng_weekly",
    )


if __name__ == "__main__":
    crawl()
