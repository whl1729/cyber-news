from news.crawler.tech_news import geekpark_crawler
from news.crawler.tech_news import hacker_news_crawler
from news.crawler.tech_news import infoq_crawler
from news.crawler.tech_news import jiqizhixin_crawler
from news.crawler.tech_news import liangziwei_crawler
from news.crawler.tech_news import new_stack_crawler
from news.crawler.tech_news import xinzhiyuan_crawler


def crawl():
    geekpark_crawler.crawl()
    hacker_news_crawler.crawl()
    infoq_crawler.crawl()
    jiqizhixin_crawler.crawl()
    liangziwei_crawler.crawl()
    new_stack_crawler.crawl()
    xinzhiyuan_crawler.crawl()


if __name__ == "__main__":
    crawl()
