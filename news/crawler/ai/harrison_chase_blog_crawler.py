import re
from datetime import datetime
from typing import List

import requests
from bs4 import BeautifulSoup

from news.util import web_crawler
from news.util.configer import config
from news.util.logger import logger
from news.util.web_parser import WebParser

HARRISON_CHASE_BLOG_URL = "https://blog.langchain.com/author/harrison/"
HARRISON_CHASE_BASE_URL = "https://blog.langchain.com"
COLLECTION_NAME = "harrison_chase_blog"


def parse_harrison_chase_date_from_image(filename: str) -> str:
    """
    Parse date from image path like '/content/images/size/w360/format/webp/2026/03/blogheader.png'

    :param filename: Image path containing YYYY/MM
    :return: ISO formatted date string (YYYY-MM-DD) or None
    """
    match = re.search(r"/(\d{4})/(\d{2})/", filename)
    if match:
        year, month = match.groups()
        return f"{year}-{month}-01"
    return None


def fetch_article_date(url: str) -> str:
    """
    Fetch the article page and extract the publication date from header.
    Date format in page: "Mar 10, 2026"

    :param url: Article URL
    :return: ISO formatted date string (YYYY-MM-DD) or None
    """
    try:
        proxies = config.get("proxies")
        resp = requests.get(url, proxies=proxies, timeout=10)
        soup = BeautifulSoup(resp.text, "lxml")

        # Find article header
        article = soup.find("article")
        if article:
            header = article.find("header")
            if header:
                text = header.get_text()
                # Match date pattern like "Mar 10, 2026"
                match = re.search(
                    r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(\d{1,2}),\s+(\d{4})",
                    text,
                    re.IGNORECASE,
                )
                if match:
                    month_str, day, year = match.groups()
                    # Convert month name to number
                    month_map = {
                        "jan": "01",
                        "feb": "02",
                        "mar": "03",
                        "apr": "04",
                        "may": "05",
                        "jun": "06",
                        "jul": "07",
                        "aug": "08",
                        "sep": "09",
                        "oct": "10",
                        "nov": "11",
                        "dec": "12",
                    }
                    month = month_map.get(month_str.lower())
                    if month:
                        return f"{year}-{month}-{day.zfill(2)}"
    except Exception as e:
        logger.warning(f"Failed to fetch article date from {url}: {e}")

    return None


class HarrisonChaseBlogParser(WebParser):
    def parse(self, resp_text: str) -> List[dict]:
        soup = BeautifulSoup(resp_text, "lxml")

        # Find all blog post entries
        blog_list = []
        for article in soup.find_all("article"):
            post = self._parse_item(article)
            if post:
                blog_list.append(post)

        logger.info(f"{len(blog_list)} harrison chase blog posts parsed")
        return blog_list

    def _parse_item(self, article) -> dict:
        try:
            # Extract title from h2 tag
            h2 = article.find("h2")
            if not h2:
                return None

            title = h2.get_text(strip=True)
            if not title:
                return None

            # Find link in the article
            link = article.find("a")
            if not link:
                return None

            href = link.get("href", "")
            if not href:
                return None

            # Handle both relative and absolute URLs
            if href.startswith("https://") or href.startswith("http://"):
                url = href
            else:
                # Relative URL
                url = f"{HARRISON_CHASE_BASE_URL}{href}"

            # Extract publication date from article page
            created_at = fetch_article_date(url)

            # Fallback: try to extract from image path
            if not created_at:
                picture = article.find("picture")
                if picture:
                    source = picture.find("source")
                    if source:
                        srcset = source.get("srcset", "")
                        if srcset:
                            sources = srcset.split(",")
                            if sources:
                                filename = sources[0].strip()
                                created_at = parse_harrison_chase_date_from_image(
                                    filename
                                )

            # Final fallback: use current time
            if not created_at:
                created_at = datetime.now().strftime("%Y-%m-%d")

            return {
                "id": title,
                "url": url,
                "created_at": created_at,
                "crawled_at": datetime.now().strftime("%Y%m%d%H%M%S"),
            }
        except Exception as e:
            logger.warning(f"Failed to parse harrison chase blog item: {e}")
            return None


def crawl():
    parser = HarrisonChaseBlogParser()
    web_crawler.crawl(
        parser, HARRISON_CHASE_BLOG_URL, COLLECTION_NAME, proxies=config["proxies"]
    )


if __name__ == "__main__":
    crawl()
