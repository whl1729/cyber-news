from news.crawler.language.go import go_blog_crawler
from news.crawler.language.go import go_news_crawler
from news.crawler.language.go import go_weekly_crawler
from news.util.configer import get_enabled_topics
from news.util.logger import logger


def crawl():
    crawlers = {
        "go_blog": go_blog_crawler,
        "go_news": go_news_crawler,
        "go_weekly": go_weekly_crawler,
    }

    enabled_topics = get_enabled_topics()
    for topic, crawler in crawlers.items():
        if enabled_topics is None or topic in enabled_topics:
            crawler.crawl()
        else:
            logger.info(f"Skipping {topic} (not in enabled_topics)")


if __name__ == "__main__":
    crawl()
