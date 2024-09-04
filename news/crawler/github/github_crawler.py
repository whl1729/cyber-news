from news.crawler.github import github_notification_crawler
from news.crawler.github import github_received_event_crawler
from news.crawler.github import github_trending_crawler


def crawl():
    github_received_event_crawler.crawl()
    github_notification_crawler.crawl()
    github_trending_crawler.crawl()


if __name__ == "__main__":
    crawl()
