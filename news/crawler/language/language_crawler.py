from news.crawler.language.cpp import cpp_crawler
from news.crawler.language.go import go_crawler
from news.crawler.language.python import python_crawler
from news.crawler.language.rust import rust_crawler


def crawl():
    cpp_crawler.crawl()
    go_crawler.crawl()
    python_crawler.crawl()
    rust_crawler.crawl()


if __name__ == "__main__":
    crawl()
