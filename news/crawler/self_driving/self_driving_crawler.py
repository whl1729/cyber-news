from news.crawler.self_driving import cv_autobot_crawler
from news.crawler.self_driving import zhineng_crawler


def crawl():
    cv_autobot_crawler.crawl()
    zhineng_crawler.crawl()


if __name__ == "__main__":
    crawl()
