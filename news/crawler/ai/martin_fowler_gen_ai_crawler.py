from datetime import datetime
from typing import List

from bs4 import BeautifulSoup

from news.util import web_crawler
from news.util.configer import config
from news.util.logger import logger
from news.util.web_parser import WebParser

MARTIN_FOWLER_GEN_AI_URL = "https://martinfowler.com/articles/exploring-gen-ai.html"
COLLECTION_NAME = "martin_fowler_gen_ai"
BASE_URL = "https://martinfowler.com/articles"


def parse_martin_fowler_date(date_str: str) -> str:
    """
    Parse date like "(04 March 2026)" -> "2026-03-04".
    """
    try:
        cleaned = date_str.strip().strip("()")
        return datetime.strptime(cleaned.strip(), "%d %B %Y").strftime("%Y-%m-%d")
    except Exception as e:
        logger.warning(f"Failed to parse martin fowler date '{date_str}': {e}")
        return datetime.now().strftime("%Y-%m-%d")


class MartinFowlerGenAIParser(WebParser):
    def parse(self, resp_text: str) -> List[dict]:
        soup = BeautifulSoup(resp_text, "lxml")

        blog_list = []
        for p in soup.find_all("p", class_="memo"):
            post = self._parse_item(p)
            if post:
                blog_list.append(post)

        logger.info(f"{len(blog_list)} martin fowler gen ai posts parsed")
        return blog_list

    def _parse_item(self, p) -> dict:
        try:
            link = p.find("a")
            if not link:
                return None

            title = link.get_text(strip=True)
            if not title:
                return None

            href = link.get("href", "")
            if not href:
                return None

            # hrefs are relative like "exploring-gen-ai/humans-and-agents.html"
            if href.startswith("http"):
                url = href
            else:
                url = f"{BASE_URL}/{href}"

            date_span = p.find("span", class_="date")
            if not date_span:
                logger.warning(f"No date span for: {title}")
                return None

            created_at = parse_martin_fowler_date(date_span.get_text(strip=True))

            return {
                "id": title,
                "url": url,
                "created_at": created_at,
                "crawled_at": datetime.now().strftime("%Y%m%d%H%M%S"),
            }
        except Exception as e:
            logger.warning(f"Failed to parse martin fowler gen ai item: {e}")
            return None


def crawl():
    parser = MartinFowlerGenAIParser()
    web_crawler.crawl(
        parser, MARTIN_FOWLER_GEN_AI_URL, COLLECTION_NAME, proxies=config["proxies"]
    )


if __name__ == "__main__":
    crawl()
