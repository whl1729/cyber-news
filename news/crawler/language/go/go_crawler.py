from news.crawler.language.go import go_blog_crawler
from news.crawler.language.go import go_news_crawler


def crawl():
    go_blog_crawler.crawl()
    go_news_crawler.crawl()


if __name__ == "__main__":
    crawl()
