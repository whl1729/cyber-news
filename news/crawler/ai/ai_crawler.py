from news.crawler.ai import claude_code_blog_crawler
from news.crawler.ai import karpathy_blog_crawler
from news.crawler.ai import openai_news_crawler
from news.util.configer import get_enabled_topics
from news.util.logger import logger


def crawl():
    crawlers = {
        "claude_code_blog": claude_code_blog_crawler,
        "openai_news": openai_news_crawler,
        "karpathy_blog": karpathy_blog_crawler,
    }

    enabled_topics = get_enabled_topics()
    for topic, crawler in crawlers.items():
        if enabled_topics is None or topic in enabled_topics:
            crawler.crawl()
        else:
            logger.info(f"Skipping {topic} (not in enabled_topics)")


if __name__ == "__main__":
    crawl()
