import requests
from crawler import github
from crawler.github.github_feed_parser import GithubFeedParser
from crawler.util import fs
from crawler.util import proxy
from crawler.util.configer import config
from crawler.util.logger import logger
from lxml import etree


class GithubCrawler(object):
    def __init__(self):
        proxy.init()

        self._email = config["github_username"]
        self._password = config["github_password"]
        self._session = requests.Session()
        self._token = self.get_token()[0]
        self._feed_parser = GithubFeedParser()

    def login(self):
        post_data = {
            "commit": "Sign in",
            "utf8": "✓",
            "authenticity_token": self._token,
            "login": self._email,
            "password": self._password,
        }
        response = self._session.post(
            github.session_url, data=post_data, headers=github.headers
        )
        if response.status_code != 200:
            logger.error(f"failed to login in: {response}")
            return False

        logger.info("Successfully logined in")
        return True

    def get_feed(self):
        response = self._session.get(github.feed_url, headers=github.headers)
        if response.status_code != 200:
            logger.error(f"failed to get news: {response}")
            return

        self._save(response.text, "feed.html")
        return self._feed_parser.parse(response.text)

    def get_token(self):
        response = self._session.get(github.login_url, headers=github.headers)
        selector = etree.HTML(response.text)
        token = selector.xpath('//*[@id="login"]/div[4]/form/input[1]/@value')
        return token

    def _save(self, html: str, dest_path: str):
        with open(fs.log_dir / dest_path, "w", encoding="utf-8") as f:
            f.write(html)


if __name__ == "__main__":
    github_crawler = GithubCrawler()
    github_crawler.login()
    github_crawler.get_feed()
