import re
from datetime import datetime
from typing import List

from bs4 import BeautifulSoup

from news.util import web_crawler
from news.util.configer import config
from news.util.logger import logger
from news.util.web_parser import WebParser

CURSOR_BLOG_URL = "https://cursor.com/blog"
COLLECTION_NAME = "cursor_blog"
BASE_URL = "https://cursor.com"


def parse_cursor_datetime(datetime_str: str) -> str:
    """
    Parse Cursor blog ISO datetime like "2026-03-27T12:00:00.000Z" -> "2026-03-27".
    """
    try:
        return datetime_str[:10]
    except Exception as e:
        logger.warning(f"Failed to parse cursor datetime '{datetime_str}': {e}")
        return datetime.now().strftime("%Y-%m-%d")


class CursorBlogParser(WebParser):
    def parse(self, resp_text: str) -> List[dict]:
        soup = BeautifulSoup(resp_text, "lxml")

        blog_list = []
        seen_urls = set()

        for a in soup.find_all("a", href=True):
            href = a.get("href", "")
            if not re.match(r"^/blog/[^/]+$", href):
                continue

            url = BASE_URL + href
            if url in seen_urls:
                continue

            # Title is in the <p> inside the article
            title_tag = a.find("p")
            if not title_tag:
                continue
            title = title_tag.get_text(strip=True)
            if not title:
                continue

            # Date is in <time datetime="ISO...">
            time_tag = a.find("time")
            if not time_tag:
                continue
            dt_attr = time_tag.get("datetime", "")
            created_at = (
                parse_cursor_datetime(dt_attr)
                if dt_attr
                else datetime.now().strftime("%Y-%m-%d")
            )

            seen_urls.add(url)
            blog_list.append(
                {
                    "id": title,
                    "url": url,
                    "created_at": created_at,
                    "crawled_at": datetime.now().strftime("%Y%m%d%H%M%S"),
                }
            )

        logger.info(f"{len(blog_list)} cursor blog posts parsed")
        return blog_list


def crawl():
    parser = CursorBlogParser()
    web_crawler.crawl(
        parser, CURSOR_BLOG_URL, COLLECTION_NAME, proxies=config["proxies"]
    )


if __name__ == "__main__":
    crawl()
