from crawler.template.template_parser import TemplateParser
from crawler.util import fs
from crawler.util import myrequests
from crawler.util.configer import config
from crawler.util.logger import logger


class GithubRepoEventCrawler:
    def __init__(self):
        self._parser = TemplateParser()
        self._headers = {
            "Authorization": f'Bearer {config["github_token"]}',
            "Accept": "application/vnd.github+json",
        }

    def crawl(self):
        events = self._get_watching_repo_events()
        # events = self._get_starred_repo_events()
        fs.save_json(events, "github_repo_events.json")
        # news_list = self._parser.parse(response.text)
        # mongo.insert_many_new("template", "id", news_list)

    def _get_starred_repo_events(self):
        return self._get_repo_events("starred")

    def _get_watching_repo_events(self):
        return self._get_repo_events("subscriptions")

    def _get_repo_events(self, repo_type: str):
        total_events = []
        repos = self._get_repos(repo_type)
        logger.info(f"{repo_type} count: {len(repos)}")
        for repo in repos:
            owner = repo["owner"]["login"]
            repo_name = repo["name"]
            cur_events = self._get_one_repo_events(owner, repo_name)
            total_events.append(cur_events)

        return total_events

    def _get_repos(self, repo_type: str):
        url = f'https://api.github.com/users/{config["github_username"]}/{repo_type}'
        repos = []
        page = 1
        while True:
            response = myrequests.get(
                url, headers=self._headers, params={"page": page, "per_page": 100}
            )
            if response.status_code != 200:
                logger.error(f"Failed to get {url}: {response.status_code}")
                break
            data = response.json()
            if not data:
                break
            repos.extend(data)
            page += 1
        return repos

    def _get_one_repo_events(self, owner, repo):
        url = f"https://api.github.com/repos/{owner}/{repo}/events"
        response = myrequests.get(url, headers=self._headers)
        if response is None:
            logger.info(f"no events for {owner}/{repo}")
            return []

        return response.json()


if __name__ == "__main__":
    crawler = GithubRepoEventCrawler()
    crawler.crawl()
