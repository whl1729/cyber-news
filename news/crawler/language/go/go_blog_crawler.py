from typing import List

from bs4 import BeautifulSoup

from news.util import timelib
from news.util import web_crawler
from news.util.configer import config
from news.util.logger import logger
from news.util.web_parser import WebParser

GO_BLOG_HOST = "https://go.dev"
GO_BLOG_URL = "https://go.dev/blog/all"


class GoBlogParser(WebParser):
    def parse(self, resp_text: str) -> List[dict]:
        soup = BeautifulSoup(resp_text, "lxml")
        blog_index = soup.find(id="blogindex")
        blog_list = []
        for blog_title in blog_index.find_all(class_="blogtitle"):
            author = blog_title.find(class_="author")
            date = blog_title.find(class_="date")
            blog_summary = blog_title.find_next_sibling(class_="blogsummary")
            blog = {
                "id": blog_title.a.string,
                "url": GO_BLOG_HOST + blog_title.a["href"],
                "author": author.text,
                "summary": blog_summary.text.strip(),
                "created_at": timelib.format_date(date.text),
                "crawled_at": timelib.now2(),
            }
            blog_list.append(blog)
        logger.info(f"{len(blog_list)} go blogs parsed")
        return blog_list


def crawl():
    parser = GoBlogParser()
    web_crawler.crawl(parser, GO_BLOG_URL, "go_blog", proxies=config["proxies"])


if __name__ == "__main__":
    crawl()
