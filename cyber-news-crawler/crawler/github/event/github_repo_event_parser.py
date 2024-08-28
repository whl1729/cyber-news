import json
from typing import List

from crawler import github
from crawler.github.event.github_event import GithubRepoEvent


class GithubRepoEventParser:
    def parse(self, resp_text: str) -> List[GithubRepoEvent]:
        events = []
        resp_list = json.loads(resp_text)
        for resp in resp_list:
            event = GithubRepoEvent(
                id=resp["id"],
                type=resp["type"],
                actor_name=resp["actor"]["login"],
                actor_url=github.host + "/" + resp["actor"]["login"],
                repo_name=resp["repo"]["name"],
                repo_url=github.host + "/" + resp["repo"]["name"],
                created_at=resp["created_at"],
            )
            events.append(event)

        return events
