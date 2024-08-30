from crawler.github import github_crawler
from crawler.hacker_news import hacker_news_crawler


def crawl():
    github_crawler.crawl()
    hacker_news_crawler.crawl()


if __name__ == "__main__":
    crawl()
