from news.crawler.language.python import pycoder_weekly_crawler
from news.crawler.language.python import python_insider_crawler


def crawl():
    python_insider_crawler.crawl()
    pycoder_weekly_crawler.crawl()


if __name__ == "__main__":
    crawl()
