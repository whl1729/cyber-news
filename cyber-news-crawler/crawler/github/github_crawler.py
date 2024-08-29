from crawler.github.event.github_user_event_crawler import GithubUserEventCrawler
from crawler.github.notification.github_notification_crawler import (
    GithubNotificationCrawler,
)
from crawler.github.trending.github_trending_crawler import GithubTrendingCrawler


def main():
    trending_crawler = GithubTrendingCrawler()
    trending_crawler.crawl()

    user_event_crawler = GithubUserEventCrawler()
    user_event_crawler.crawl()

    notification_crawler = GithubNotificationCrawler()
    notification_crawler.crawl()


if __name__ == "__main__":
    main()
