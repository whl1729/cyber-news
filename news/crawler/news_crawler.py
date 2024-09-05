from news.crawler.blog import blog_crawler
from news.crawler.github import github_crawler
from news.crawler.hacker_news import hacker_news_crawler
from news.crawler.language import language_crawler


def crawl():
    github_crawler.crawl()
    hacker_news_crawler.crawl()
    language_crawler.crawl()
    blog_crawler.crawl()


if __name__ == "__main__":
    crawl()
