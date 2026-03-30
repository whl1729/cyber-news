from news.crawler.language.cpp import isocpp_blog_crawler
from news.util.configer import get_enabled_topics
from news.util.logger import logger


def crawl():
    crawlers = {
        "isocpp_blog": isocpp_blog_crawler,
    }

    enabled_topics = get_enabled_topics()
    for topic, crawler in crawlers.items():
        if enabled_topics is None or topic in enabled_topics:
            crawler.crawl()
        else:
            logger.info(f"Skipping {topic} (not in enabled_topics)")


if __name__ == "__main__":
    crawl()
