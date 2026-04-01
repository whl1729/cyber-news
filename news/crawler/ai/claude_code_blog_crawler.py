from typing import List

from bs4 import BeautifulSoup

from news.util import timelib
from news.util import web_crawler
from news.util.configer import config
from news.util.logger import logger
from news.util.web_parser import WebParser

CLAUDE_CODE_BLOG_URL = "https://claude.com/blog"


class ClaudeCodeBlogParser(WebParser):
    def parse(self, resp_text: str) -> List[dict]:
        soup = BeautifulSoup(resp_text, "lxml")

        blog_list = []
        seen_urls = set()

        # 方法1：查找 marquee_cms_blog_list_item（首页轮播区域）
        marquee_items = soup.find_all(
            "div",
            class_=lambda x: x
            and "marquee_cms_blog_list_item" in x
            and "w-dyn-item" in x,
        )
        for article in marquee_items:
            blog = self._parse_marquee_item(article)
            if blog and blog["url"] not in seen_urls:
                blog_list.append(blog)
                seen_urls.add(blog["url"])

        # 方法2：查找 blog_cms_item（主要博客列表）
        cms_items = soup.find_all(
            "div", class_=lambda x: x and "blog_cms_item" in x and "w-dyn-item" in x
        )
        for article in cms_items:
            blog = self._parse_cms_item(article)
            if blog and blog["url"] not in seen_urls:
                blog_list.append(blog)
                seen_urls.add(blog["url"])

        logger.info(f"{len(blog_list)} claude code blogs parsed")
        return blog_list

    def _parse_marquee_item(self, article) -> dict:
        """解析首页轮播区域的博客项"""
        try:
            title_elem = article.find(["h2", "h3", "h4"])
            if not title_elem:
                return None

            title = title_elem.get_text(strip=True)

            link_elem = article.find("a", href=lambda x: x and "/blog/" in x)
            if not link_elem:
                return None

            url = link_elem.get("href", "")
            if "/category/" in url:
                return None

            if url and not url.startswith("http"):
                url = f"https://claude.com{url}"

            # 日期在 caption 样式的 div 中，格式：March 12, 2026
            date_elem = article.find("div", class_=lambda x: x and "caption" in x)
            date = date_elem.get_text(strip=True) if date_elem else ""

            return {
                "id": title,
                "url": url,
                "created_at": timelib.format_date_3(date) if date else timelib.today(),
                "crawled_at": timelib.now2(),
            }
        except Exception as e:
            logger.warning(f"Failed to parse marquee item: {e}")
            return None

    def _parse_cms_item(self, article) -> dict:
        """解析主要博客列表的博客项"""
        try:
            # 标题在 card_blog_title div 中
            title_elem = article.find(
                "div", class_=lambda x: x and "card_blog_title" in x
            )
            if not title_elem:
                return None

            title = title_elem.get_text(strip=True)

            link_elem = article.find("a", href=lambda x: x and "/blog/" in x)
            if not link_elem:
                return None

            url = link_elem.get("href", "")
            if "/category/" in url:
                return None

            if url and not url.startswith("http"):
                url = f"https://claude.com{url}"

            # 日期在第一个 caption div 中（包含 u-mb-1-5），格式：Mar 30, 2026（缩写月份 + 逗号）
            date_elem = article.find(
                "div", class_=lambda x: x and "caption" in x and "u-mb-1-5" in x
            )
            date = date_elem.get_text(strip=True) if date_elem else ""

            return {
                "id": title,
                "url": url,
                "created_at": timelib.format_date_6(date) if date else timelib.today(),
                "crawled_at": timelib.now2(),
            }
        except Exception as e:
            logger.warning(f"Failed to parse cms item: {e}")
            return None


def crawl():
    parser = ClaudeCodeBlogParser()
    web_crawler.crawl(
        parser, CLAUDE_CODE_BLOG_URL, "claude_code_blog", proxies=config["proxies"]
    )


if __name__ == "__main__":
    crawl()
