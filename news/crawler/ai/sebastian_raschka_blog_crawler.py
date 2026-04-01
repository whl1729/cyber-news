from typing import List

from bs4 import BeautifulSoup

from news.util import timelib
from news.util import web_crawler
from news.util.configer import config
from news.util.logger import logger
from news.util.web_parser import WebParser

SEBASTIAN_RASCHKA_BLOG_URL = "https://sebastianraschka.com"
SEBASTIAN_RASCHKA_BASE_URL = "https://sebastianraschka.com"
COLLECTION_NAME = "sebastian_raschka_blog"


class SebastianRaschkaBlogParser(WebParser):
    def parse(self, resp_text: str) -> List[dict]:
        soup = BeautifulSoup(resp_text, "lxml")

        # Find all blog post entries
        posts_div = soup.find("article", class_="posts-by-year")
        if not posts_div:
            logger.warning("No posts-by-year section found on Sebastian Raschka blog")
            return []

        blog_list = []
        for post_entry in posts_div.find_all("div", class_="post-entry"):
            post = self._parse_item(post_entry)
            if post:
                blog_list.append(post)

        logger.info(f"{len(blog_list)} sebastian raschka blog posts parsed")
        return blog_list

    def _parse_item(self, post_entry) -> dict:
        try:
            # Find the post details div
            post_details = post_entry.find("div", class_="post-details")
            if not post_details:
                return None

            # Extract date
            date_elem = post_details.find("p", class_="post-date")
            if not date_elem:
                return None

            date_str = date_elem.get_text(strip=True)
            created_at = timelib.format_date_6(date_str)

            # Extract title and URL
            title_elem = post_details.find("h3", class_="post-title")
            if not title_elem:
                return None

            link_elem = title_elem.find("a")
            if not link_elem:
                return None

            title = link_elem.get_text(strip=True)
            href = link_elem.get("href", "")
            if not href:
                return None

            # Handle both absolute and relative URLs
            if href.startswith("https://") or href.startswith("http://"):
                url = href
            elif href.startswith("/"):
                url = f"{SEBASTIAN_RASCHKA_BASE_URL}{href}"
            else:
                # Assume relative URL without leading slash
                url = f"{SEBASTIAN_RASCHKA_BASE_URL}/{href}"

            # Extract optional description
            desc_elem = post_details.find("p", class_="post-description")
            description = desc_elem.get_text(strip=True) if desc_elem else ""

            return {
                "id": title,
                "url": url,
                "created_at": created_at,
                "crawled_at": timelib.now2(),
            }
        except Exception as e:
            logger.warning(f"Failed to parse sebastian raschka blog item: {e}")
            return None


def crawl():
    parser = SebastianRaschkaBlogParser()
    web_crawler.crawl(
        parser, SEBASTIAN_RASCHKA_BLOG_URL, COLLECTION_NAME, proxies=config["proxies"]
    )


if __name__ == "__main__":
    crawl()
