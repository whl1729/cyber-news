from news.crawler.tech_news import geekpark_crawler
from news.crawler.tech_news import hacker_news_crawler
from news.crawler.tech_news import infoq_crawler
from news.crawler.tech_news import jiqizhixin_crawler
from news.crawler.tech_news import liangziwei_crawler
from news.crawler.tech_news import new_stack_crawler
from news.crawler.tech_news import xinzhiyuan_crawler
from news.util.configer import get_enabled_topics
from news.util.logger import logger


def crawl():
    crawlers = {
        "geekpark": geekpark_crawler,
        "hacker_news": hacker_news_crawler,
        "infoq": infoq_crawler,
        "jiqizhixin": jiqizhixin_crawler,
        "liangziwei": liangziwei_crawler,
        "new_stack": new_stack_crawler,
        "xinzhiyuan": xinzhiyuan_crawler,
    }

    enabled_topics = get_enabled_topics()
    for topic, crawler in crawlers.items():
        if enabled_topics is None or topic in enabled_topics:
            crawler.crawl()
        else:
            logger.info(f"Skipping {topic} (not in enabled_topics)")


if __name__ == "__main__":
    crawl()
