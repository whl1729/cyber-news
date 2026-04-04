from datetime import datetime
from typing import List

from bs4 import BeautifulSoup

from news.util import timelib
from news.util import web_crawler
from news.util.configer import config
from news.util.logger import logger
from news.util.web_parser import WebParser

DHH_BLOG_ATOM_URL = "https://world.hey.com/dhh/feed.atom"
COLLECTION_NAME = "dhh_blog"


def parse_iso_date(date_str: str) -> str:
    try:
        dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d")
    except Exception as e:
        logger.warning(f"Failed to parse date '{date_str}': {e}")
        return datetime.now().strftime("%Y-%m-%d")


class DhhBlogParser(WebParser):
    def parse(self, resp_text: str) -> List[dict]:
        soup = BeautifulSoup(resp_text, "xml")

        blog_list = []
        entries = soup.find_all("entry")
        for entry in entries:
            post = self._parse_item(entry)
            if post:
                blog_list.append(post)

        logger.info(f"{len(blog_list)} dhh blog posts parsed")
        return blog_list

    def _parse_item(self, entry) -> dict:
        try:
            title_tag = entry.find("title")
            link_tag = entry.find("link")
            published_tag = entry.find("published")

            if not title_tag or not link_tag:
                return None

            title = title_tag.get_text(strip=True)
            url = link_tag.get("href", "")

            if not title or not url:
                return None

            if published_tag:
                created_at = parse_iso_date(published_tag.get_text(strip=True))
            else:
                created_at = datetime.now().strftime("%Y-%m-%d")

            return {
                "id": title,
                "url": url,
                "created_at": created_at,
                "crawled_at": timelib.now2(),
            }
        except Exception as e:
            logger.warning(f"Failed to parse dhh blog item: {e}")
            return None


def crawl():
    parser = DhhBlogParser()
    web_crawler.crawl(
        parser,
        DHH_BLOG_ATOM_URL,
        COLLECTION_NAME,
        proxies=config["proxies"],
    )


if __name__ == "__main__":
    crawl()
