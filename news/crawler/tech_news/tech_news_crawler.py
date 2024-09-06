from news.crawler.tech_news import infoq_crawler
from news.crawler.tech_news import new_stack_crawler


def crawl():
    infoq_crawler.crawl()
    new_stack_crawler.crawl()


if __name__ == "__main__":
    crawl()
