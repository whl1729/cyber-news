from news.crawler.blog import blog_crawler
from news.crawler.github import github_crawler
from news.crawler.language import language_crawler
from news.crawler.self_driving import self_driving_crawler
from news.crawler.tech_news import tech_news_crawler


def crawl():
    blog_crawler.crawl()
    github_crawler.crawl()
    language_crawler.crawl()
    self_driving_crawler.crawl()
    tech_news_crawler.crawl()


if __name__ == "__main__":
    crawl()
