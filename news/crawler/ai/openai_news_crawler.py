import traceback
from typing import List

from bs4 import BeautifulSoup

from news.util import fs
from news.util import myrequests
from news.util import timelib
from news.util.configer import config
from news.util.logger import logger
from news.util.mongodb import mongo
from news.util.web_parser import WebParser

OPENAI_NEWS_URL = "https://openai.com/zh-Hans-CN/news/"
OPENAI_BASE_URL = "https://openai.com/zh-Hans-CN"
COLLECTION_NAME = "openai_news"


class OpenAINewsParser(WebParser):
    def parse(self, resp_text: str) -> List[dict]:
        soup = BeautifulSoup(resp_text, "lxml")

        news_list = []
        seen_urls = set()

        # 查找所有带 aria-label 的 <a> 标签（新闻条目链接）
        for a_tag in soup.find_all("a", attrs={"aria-label": True}):
            news = self._parse_item(a_tag)
            if news and news["url"] not in seen_urls:
                news_list.append(news)
                seen_urls.add(news["url"])

        logger.info(f"{len(news_list)} openai news parsed")
        return news_list

    def _parse_item(self, a_tag) -> dict:
        try:
            aria_label = a_tag.get("aria-label", "")
            parts = aria_label.split(" - ")
            if len(parts) < 2:
                return None

            title = parts[0].strip()
            if not title:
                return None

            href = a_tag.get("href", "")
            if not href or "/index/" not in href:
                return None

            url = f"{OPENAI_BASE_URL}{href}" if not href.startswith("http") else href

            time_tag = a_tag.find("time", attrs={"datetime": True})
            if not time_tag:
                logger.warning(f"No time tag found for: {title}")
                return None

            date_str = time_tag.get("datetime", "")[:10]

            return {
                "id": title,
                "url": url,
                "created_at": date_str,
                "crawled_at": timelib.now2(),
            }
        except Exception as e:
            logger.warning(f"Failed to parse openai news item: {e}")
            return None


def crawl():
    response = myrequests.get_with_cffi(
        OPENAI_NEWS_URL, proxies=config["proxies"], timeout=15
    )
    if response is None:
        logger.error(f"No response from {OPENAI_NEWS_URL}")
        return False

    resp_text = response.text
    fs.save_response_text(resp_text, COLLECTION_NAME)

    try:
        parser = OpenAINewsParser()
        news_list = parser.parse(resp_text)
    except Exception as e:
        logger.error(
            f"Failed to parse openai news: {e}, trace: {traceback.format_exc()}"
        )
        return False

    count = mongo.insert_many_new(COLLECTION_NAME, "id", news_list)
    logger.info(f"{count} openai news inserted")
    return True


if __name__ == "__main__":
    crawl()
