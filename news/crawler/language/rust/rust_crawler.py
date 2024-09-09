from news.crawler.language.rust import rust_blog_crawler
from news.crawler.language.rust import rust_weekly_crawler


def crawl():
    rust_blog_crawler.crawl()
    rust_weekly_crawler.crawl()


if __name__ == "__main__":
    crawl()
