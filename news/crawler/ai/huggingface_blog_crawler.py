from datetime import datetime
from typing import List

from bs4 import BeautifulSoup

from news.util import timelib
from news.util import web_crawler
from news.util.configer import config
from news.util.logger import logger
from news.util.web_parser import WebParser

HUGGINGFACE_BLOG_URL = "https://huggingface.co/blog"
COLLECTION_NAME = "huggingface_blog"
BASE_URL = "https://huggingface.co"


def parse_huggingface_date(datetime_str: str) -> str:
    try:
        dt = datetime.fromisoformat(datetime_str.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d")
    except Exception as e:
        logger.warning(f"Failed to parse date '{datetime_str}': {e}")
        return datetime.now().strftime("%Y-%m-%d")


class HuggingfaceBlogParser(WebParser):
    def parse(self, resp_text: str) -> List[dict]:
        soup = BeautifulSoup(resp_text, "lxml")

        blog_list = []
        articles = soup.find_all("article")
        for article in articles:
            post = self._parse_item(article)
            if post:
                blog_list.append(post)

        logger.info(f"{len(blog_list)} huggingface blog posts parsed")
        return blog_list

    def _parse_item(self, article) -> dict:
        try:
            link_tag = article.find("a", href=lambda h: h and h.startswith("/blog/"))
            if not link_tag:
                return None

            href = link_tag.get("href", "")
            if not href or href == "/blog" or href == "/blog/community":
                return None

            url = BASE_URL + href if href.startswith("/") else href

            title_tag = (
                link_tag.find("h3") or link_tag.find("h2") or link_tag.find("h4")
            )
            if not title_tag:
                return None

            title = title_tag.get_text(strip=True)
            if not title:
                return None

            time_tag = article.find("time")
            if time_tag:
                datetime_attr = time_tag.get("datetime")
                if datetime_attr:
                    created_at = parse_huggingface_date(datetime_attr)
                else:
                    created_at = datetime.now().strftime("%Y-%m-%d")
            else:
                created_at = datetime.now().strftime("%Y-%m-%d")

            return {
                "id": title,
                "url": url,
                "created_at": created_at,
                "crawled_at": timelib.now2(),
            }
        except Exception as e:
            logger.warning(f"Failed to parse huggingface blog item: {e}")
            return None


def crawl():
    parser = HuggingfaceBlogParser()
    web_crawler.crawl(
        parser,
        HUGGINGFACE_BLOG_URL,
        COLLECTION_NAME,
        proxies=config["proxies"],
        use_selenium=False,
    )


if __name__ == "__main__":
    crawl()
