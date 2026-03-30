from news.crawler.github import github_notification_crawler
from news.crawler.github import github_received_event_crawler
from news.crawler.github import github_trending_crawler
from news.util.configer import get_enabled_topics
from news.util.logger import logger


def crawl():
    crawlers = {
        "github_received_event": github_received_event_crawler,
        "github_notification": github_notification_crawler,
        "github_trending": github_trending_crawler,
    }

    enabled_topics = get_enabled_topics()
    for topic, crawler in crawlers.items():
        if enabled_topics is None or topic in enabled_topics:
            crawler.crawl()
        else:
            logger.info(f"Skipping {topic} (not in enabled_topics)")


if __name__ == "__main__":
    crawl()
