from datetime import datetime
from typing import List

from bs4 import BeautifulSoup

from news.util import timelib
from news.util import web_crawler
from news.util.configer import config
from news.util.logger import logger
from news.util.web_parser import WebParser

MATT_SHUMER_BLOG_URL = "https://shumer.dev/blog"
COLLECTION_NAME = "matt_shumer_blog"


def parse_date(date_str: str) -> str:
    """Parse date from format like 'Feb 9, 2026'"""
    try:
        dt = datetime.strptime(date_str, "%b %d, %Y")
        return dt.strftime("%Y-%m-%d")
    except Exception as e:
        logger.warning(f"Failed to parse date '{date_str}': {e}")
        return datetime.now().strftime("%Y-%m-%d")


class MattShumerBlogParser(WebParser):
    def parse(self, resp_text: str) -> List[dict]:
        soup = BeautifulSoup(resp_text, "html.parser")
        blog_list = []
        articles = soup.find_all("article", class_="post")
        for article in articles:
            post = self._parse_item(article)
            if post:
                blog_list.append(post)
        logger.info(f"{len(blog_list)} matt shumer blog posts parsed")
        return blog_list

    def _parse_item(self, article) -> dict:
        try:
            title_tag = article.find("h2")
            link_tag = article.find("a")
            meta_tag = article.find("div", class_="post-meta")
            if not title_tag or not link_tag:
                return None
            title = title_tag.get_text(strip=True)
            url = link_tag.get("href", "")
            if url and not url.startswith("http"):
                url = f"https://shumer.dev{url}"
            if not title or not url:
                return None
            created_at = datetime.now().strftime("%Y-%m-%d")
            if meta_tag:
                meta_text = meta_tag.get_text(strip=True)
                parts = meta_text.split("•")
                if len(parts) >= 2:
                    date_str = parts[1].strip()
                    created_at = parse_date(date_str)
            return {
                "id": title,
                "url": url,
                "created_at": created_at,
                "crawled_at": timelib.now2(),
            }
        except Exception as e:
            logger.warning(f"Failed to parse matt shumer blog item: {e}")
            return None


def crawl():
    parser = MattShumerBlogParser()
    web_crawler.crawl(
        parser, MATT_SHUMER_BLOG_URL, COLLECTION_NAME, proxies=config["proxies"]
    )


if __name__ == "__main__":
    crawl()
