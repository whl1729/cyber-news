from datetime import datetime
from typing import List

from bs4 import BeautifulSoup

from news.util import web_crawler
from news.util.configer import config
from news.util.logger import logger
from news.util.web_parser import WebParser

YOHEI_NAKAJIMA_BLOG_URL = "https://yoheinakajima.com/blog/"
COLLECTION_NAME = "yohei_nakajima_blog"


def parse_yohei_date(date_str: str) -> str:
    """
    Parse date from format like "December 5, 2025" to YYYY-MM-DD.

    :param date_str: Date string from the blog
    :return: ISO formatted date string (YYYY-MM-DD)
    """
    try:
        # Parse date like "December 5, 2025"
        dt = datetime.strptime(date_str, "%B %d, %Y")
        return dt.strftime("%Y-%m-%d")
    except Exception as e:
        logger.warning(f"Failed to parse date '{date_str}': {e}")
        return datetime.now().strftime("%Y-%m-%d")


class YoheiNakajimaBlogParser(WebParser):
    def parse(self, resp_text: str) -> List[dict]:
        soup = BeautifulSoup(resp_text, "lxml")

        # Find all blog post entries in the wp-block-latest-posts list
        blog_list = []
        posts_ul = soup.find("ul", class_="wp-block-latest-posts__list")
        if posts_ul:
            for li in posts_ul.find_all("li"):
                post = self._parse_item(li)
                if post:
                    blog_list.append(post)

        logger.info(f"{len(blog_list)} yohei nakajima blog posts parsed")
        return blog_list

    def _parse_item(self, li) -> dict:
        try:
            # Extract title and URL from <a> tag
            link = li.find("a", class_="wp-block-latest-posts__post-title")
            if not link:
                return None

            title = link.get_text(strip=True)
            url = link.get("href", "")

            if not title or not url:
                return None

            # Extract date from <time> tag
            time_tag = li.find("time", class_="wp-block-latest-posts__post-date")
            if time_tag:
                date_str = time_tag.get_text(strip=True)
                created_at = parse_yohei_date(date_str)
            else:
                created_at = datetime.now().strftime("%Y-%m-%d")

            return {
                "id": title,
                "url": url,
                "created_at": created_at,
                "crawled_at": datetime.now().strftime("%Y%m%d%H%M%S"),
            }
        except Exception as e:
            logger.warning(f"Failed to parse yohei nakajima blog item: {e}")
            return None


def crawl():
    parser = YoheiNakajimaBlogParser()
    web_crawler.crawl(
        parser, YOHEI_NAKAJIMA_BLOG_URL, COLLECTION_NAME, proxies=config["proxies"]
    )


if __name__ == "__main__":
    crawl()
