from news.crawler import news_crawler
from news.reporter import news_reporter


def generate():
    news_crawler.crawl()
    news_reporter.report()


if __name__ == "__main__":
    generate()
