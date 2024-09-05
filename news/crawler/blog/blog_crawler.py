from news.crawler.blog import infoq_crawler
from news.crawler.blog import new_stack_crawler
from news.crawler.blog import ruanyifeng_weekly_crawler


def crawl():
    infoq_crawler.crawl()
    ruanyifeng_weekly_crawler.crawl()
    new_stack_crawler.crawl()


if __name__ == "__main__":
    crawl()
