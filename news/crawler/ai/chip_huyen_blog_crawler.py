from typing import List

from bs4 import BeautifulSoup

from news.util import timelib
from news.util import web_crawler
from news.util.configer import config
from news.util.logger import logger
from news.util.web_parser import WebParser

CHIP_HUYEN_BLOG_URL = "https://huyenchip.com/blog/"
CHIP_HUYEN_BASE_URL = "https://huyenchip.com"
COLLECTION_NAME = "chip_huyen_blog"


class ChipHuyenBlogParser(WebParser):
    def parse(self, resp_text: str) -> List[dict]:
        soup = BeautifulSoup(resp_text, "lxml")

        posts_ul = soup.find("ul", class_="post-list")
        if not posts_ul:
            logger.warning("No post list found on Chip Huyen blog page")
            return []

        blog_list = []
        for li in posts_ul.find_all("li"):
            post = self._parse_item(li)
            if post:
                blog_list.append(post)

        logger.info(f"{len(blog_list)} chip huyen blog posts parsed")
        return blog_list

    def _parse_item(self, li) -> dict:
        try:
            date_elem = li.find("span", class_="post-meta")
            if not date_elem:
                return None

            date_str = date_elem.get_text(strip=True)
            created_at = timelib.format_date_6(date_str)

            link_elem = li.find("a", class_="post-link")
            if not link_elem:
                return None

            title = link_elem.get_text(strip=True)
            href = link_elem.get("href", "")
            if not href:
                return None

            url = f"{CHIP_HUYEN_BASE_URL}{href}"

            return {
                "id": title,
                "url": url,
                "created_at": created_at,
                "crawled_at": timelib.now2(),
            }
        except Exception as e:
            logger.warning(f"Failed to parse chip huyen blog item: {e}")
            return None


def crawl():
    parser = ChipHuyenBlogParser()
    web_crawler.crawl(
        parser, CHIP_HUYEN_BLOG_URL, COLLECTION_NAME, proxies=config["proxies"]
    )


if __name__ == "__main__":
    crawl()
