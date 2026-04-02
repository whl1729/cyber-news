from datetime import datetime
from typing import List

from bs4 import BeautifulSoup

from news.util import web_crawler
from news.util.configer import config
from news.util.logger import logger
from news.util.web_parser import WebParser

DEEPMIND_BLOG_URL = "https://deepmind.google/blog/"
COLLECTION_NAME = "deepmind_blog"
BASE_URL = "https://deepmind.google"


def parse_deepmind_date(date_str: str) -> str:
    try:
        dt = datetime.strptime(date_str.strip(), "%B %Y")
        return dt.strftime("%Y-%m-01")
    except Exception as e:
        logger.warning(f"Failed to parse date '{date_str}': {e}")
        return datetime.now().strftime("%Y-%m-01")


class DeepmindBlogParser(WebParser):
    def parse(self, resp_text: str) -> List[dict]:
        soup = BeautifulSoup(resp_text, "lxml")

        blog_list = []
        articles = soup.find_all("article", class_="card-blog")
        for article in articles:
            post = self._parse_item(article)
            if post:
                blog_list.append(post)

        logger.info(f"{len(blog_list)} deepmind blog posts parsed")
        return blog_list

    def _parse_item(self, article) -> dict:
        try:
            title_tag = article.find("h3", class_="card__title")
            if not title_tag:
                return None
            title = title_tag.get_text(strip=True)
            if not title:
                return None

            link_tag = article.find("a", class_="card__overlay-link")
            if not link_tag:
                return None
            href = link_tag.get("href", "")
            if not href:
                return None
            if href.startswith("/"):
                url = BASE_URL + href
            else:
                url = href

            time_tag = article.find("time")
            if time_tag:
                date_str = time_tag.get("datetime") or time_tag.get_text(strip=True)
                created_at = parse_deepmind_date(date_str)
            else:
                created_at = datetime.now().strftime("%Y-%m-01")

            return {
                "id": title,
                "url": url,
                "created_at": created_at,
                "crawled_at": datetime.now().strftime("%Y%m%d%H%M%S"),
            }
        except Exception as e:
            logger.warning(f"Failed to parse deepmind blog item: {e}")
            return None


def crawl():
    parser = DeepmindBlogParser()
    web_crawler.crawl(
        parser, DEEPMIND_BLOG_URL, COLLECTION_NAME, proxies=config["proxies"]
    )


if __name__ == "__main__":
    crawl()
