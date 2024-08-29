import json
from typing import List

from crawler import github
from crawler.util.logger import logger


class GithubNotificationParser:
    def parse(self, resp_text: str) -> List[dict]:
        news_list = []
        notifications = json.loads(resp_text)
        for i, notification in enumerate(notifications):
            news = {
                "id": notification["id"],
                "repo": notification["repository"]["full_name"],
                "subject": notification["subject"]["title"],
                "type": notification["subject"]["type"],
                "url": self._get_url(notification),
                "updated_at": notification["updated_at"],
            }

            news_list.append(news)
            logger.info(f"{i+1}. notification: {news}")

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
