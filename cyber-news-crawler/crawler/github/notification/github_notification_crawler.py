from crawler import github
from crawler.github.notification.github_notification_parser import (
    GithubNotificationParser,
)
from crawler.util.web_crawler import WebCrawler


class GithubNotificationCrawler(WebCrawler):
    def __init__(self):
        parser = GithubNotificationParser()
        super().__init__(
            parser,
            github.notification_url,
            "github_notifications",
            headers=github.headers,
        )


if __name__ == "__main__":
    notification_crawler = GithubNotificationCrawler()
    notification_crawler.crawl()
