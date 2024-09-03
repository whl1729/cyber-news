from crawler.blog import ruanyifeng_weekly_crawler
from crawler.github import github_crawler
from crawler.hacker_news import hacker_news_crawler
from crawler.language import language_crawler


def crawl():
    github_crawler.crawl()
    hacker_news_crawler.crawl()
    language_crawler.crawl()
    ruanyifeng_weekly_crawler.crawl()


if __name__ == "__main__":
    crawl()
