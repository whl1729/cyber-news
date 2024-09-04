from crawler.language.cpp import cpp_crawler
from crawler.language.go import go_crawler
from crawler.language.rust import rust_crawler


def crawl():
    cpp_crawler.crawl()
    go_crawler.crawl()
    rust_crawler.crawl()


if __name__ == "__main__":
    crawl()
