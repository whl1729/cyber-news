import json
from typing import List

from crawler import github
from crawler.util import web_crawler
from crawler.util.logger import logger


class GithubNotificationParser:
    def parse(self, resp_text: str) -> List[dict]:
        news_list = []
        notifications = json.loads(resp_text)
        for notification in notifications:
            news = {
                "id": notification["id"],
                "repo": notification["repository"]["full_name"],
                "subject": notification["subject"]["title"],
                "type": notification["subject"]["type"],
                "url": self._get_url(notification),
                "updated_at": notification["updated_at"],
            }

            news_list.append(news)

        logger.info(f"{len(notifications)} github notifications parsed")
        return news_list

    @staticmethod
    def _get_url(notification: dict) -> str:
        url = notification["subject"]["url"]
        if url:
            return url.replace("api.github.com/repos", "github.com")

        url = github.host + "/" + notification["repository"]["full_name"]
        if notification["subject"]["type"] == "Discussion":
            return url + "/discussions"

        return url


def crawl():
    parser = GithubNotificationParser()
    web_crawler.crawl(
        parser,
        github.notification_url,
        "github_notifications",
        headers=github.headers,
    )


if __name__ == "__main__":
    crawl()
