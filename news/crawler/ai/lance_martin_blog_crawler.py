from datetime import datetime
from typing import List

from bs4 import BeautifulSoup

from news.util import web_crawler
from news.util.configer import config
from news.util.logger import logger
from news.util.web_parser import WebParser

LANCE_MARTIN_BLOG_URL = "https://rlancemartin.github.io"
COLLECTION_NAME = "lance_martin_blog"


def parse_lance_martin_date(date_str: str) -> str:
    """
    Parse date like "Jan 9, 2026" -> "2026-01-09".
    """
    try:
        return datetime.strptime(date_str.strip(), "%b %d, %Y").strftime("%Y-%m-%d")
    except Exception as e:
        logger.warning(f"Failed to parse lance martin date '{date_str}': {e}")
        return datetime.now().strftime("%Y-%m-%d")


class LanceMartinBlogParser(WebParser):
    def parse(self, resp_text: str) -> List[dict]:
        soup = BeautifulSoup(resp_text, "lxml")

        blog_list = []
        post_list = soup.find("ul", class_="post-list")
        if not post_list:
            logger.warning("No post-list found on lance martin blog page")
            return blog_list

        for li in post_list.find_all("li"):
            post = self._parse_item(li)
            if post:
                blog_list.append(post)

        logger.info(f"{len(blog_list)} lance martin blog posts parsed")
        return blog_list

    def _parse_item(self, li) -> dict:
        try:
            link = li.find("a", class_="post-link")
            if not link:
                return None

            title = link.get_text(strip=True)
            if not title:
                return None

            href = link.get("href", "")
            if not href:
                return None

            if href.startswith("http"):
                url = href
            else:
                url = LANCE_MARTIN_BLOG_URL + href

            date_span = li.find("span", class_="post-meta")
            if not date_span:
                logger.warning(f"No date span for: {title}")
                return None

            created_at = parse_lance_martin_date(date_span.get_text(strip=True))

            return {
                "id": title,
                "url": url,
                "created_at": created_at,
                "crawled_at": datetime.now().strftime("%Y%m%d%H%M%S"),
            }
        except Exception as e:
            logger.warning(f"Failed to parse lance martin blog item: {e}")
            return None


def crawl():
    parser = LanceMartinBlogParser()
    web_crawler.crawl(
        parser, LANCE_MARTIN_BLOG_URL, COLLECTION_NAME, proxies=config["proxies"]
    )


if __name__ == "__main__":
    crawl()
