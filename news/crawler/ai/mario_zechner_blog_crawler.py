from datetime import datetime
from email.utils import parsedate_to_datetime
from typing import List

from bs4 import BeautifulSoup

from news.util import timelib
from news.util import web_crawler
from news.util.configer import config
from news.util.logger import logger
from news.util.web_parser import WebParser

MARIO_ZECHNER_BLOG_RSS_URL = "https://mariozechner.at/rss.xml"
COLLECTION_NAME = "mario_zechner_blog"


def parse_rfc2822_date(date_str: str) -> str:
    try:
        dt = parsedate_to_datetime(date_str)
        return dt.strftime("%Y-%m-%d")
    except Exception as e:
        logger.warning(f"Failed to parse date '{date_str}': {e}")
        return datetime.now().strftime("%Y-%m-%d")


class MarioZechnerBlogParser(WebParser):
    def parse(self, resp_text: str) -> List[dict]:
        soup = BeautifulSoup(resp_text, "xml")

        blog_list = []
        items = soup.find_all("item")
        for item in items:
            post = self._parse_item(item)
            if post:
                blog_list.append(post)

        logger.info(f"{len(blog_list)} mario zechner blog posts parsed")
        return blog_list

    def _parse_item(self, item) -> dict:
        try:
            title_tag = item.find("title")
            link_tag = item.find("link")
            pub_date_tag = item.find("pubDate")

            if not title_tag or not link_tag:
                return None

            title = title_tag.get_text(strip=True)
            url = link_tag.get_text(strip=True)

            if not title or not url:
                return None

            if pub_date_tag:
                created_at = parse_rfc2822_date(pub_date_tag.get_text(strip=True))
            else:
                created_at = datetime.now().strftime("%Y-%m-%d")

            return {
                "id": title,
                "url": url,
                "created_at": created_at,
                "crawled_at": timelib.now2(),
            }
        except Exception as e:
            logger.warning(f"Failed to parse mario zechner blog item: {e}")
            return None


def crawl():
    parser = MarioZechnerBlogParser()
    web_crawler.crawl(
        parser,
        MARIO_ZECHNER_BLOG_RSS_URL,
        COLLECTION_NAME,
        proxies=config["proxies"],
    )


if __name__ == "__main__":
    crawl()
