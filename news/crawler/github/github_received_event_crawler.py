import json
from typing import List

from news.crawler import github
from news.util import web_crawler
from news.util.logger import logger


class GithubReceivedEventParser:
    def parse(self, resp_text: str) -> List[dict]:
        events = []
        resp_list = json.loads(resp_text)
        for resp in resp_list:
            event = {
                "id": resp["id"],
                "type": resp["type"],
                "actor_name": resp["actor"]["login"],
                "actor_url": github.host + "/" + resp["actor"]["login"],
                "repo_name": resp["repo"]["name"],
                "repo_url": github.host + "/" + resp["repo"]["name"],
                "created_at": resp["created_at"],
            }
            events.append(event)

        logger.info(f"{len(events)} github received events parsed")
        return events


def crawl():
    parser = GithubReceivedEventParser()
    web_crawler.crawl(
        parser,
        github.received_event_url,
        "github_received_events",
        headers=github.headers,
    )


if __name__ == "__main__":
    crawl()
