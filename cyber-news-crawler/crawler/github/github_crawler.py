import requests
from crawler import github
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

    def login(self):
        self.get_dynamics()
        self.get_profile()

    def get_dynamics(self):
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
            logger.error(f"failed to post session: {response}")
            return

        html = response.text
        self._save(html, "dynamics.html")
        selector = etree.HTML(html)
        dynamics = selector.xpath(
            '//div[contains(@class, "news")]//div[contains(@class, "alert")]'
        )
        logger.info("dynamic:")
        for item in dynamics:
            dynamic = " ".join(item.xpath('.//div[@class="title"]//text()')).strip()
            logger.info(dynamic)

    def get_profile(self):
        response = self._session.get(github.profile_url, headers=github.headers)
        if response.status_code != 200:
            logger.error(f"failed to get profile: {response}")
            return

        html = response.text
        selector = etree.HTML(html)
        name = selector.xpath('//input[@id="user_profile_name"]/@value')[0]
        email = selector.xpath(
            '//select[@id="user_profile_email"]/option[@value!=""]/text()'
        )[0]
        logger.info(f"name: {name}, email: {email}")

    def get_news(self):
        response = self._session.get(github.news_url, headers=github.headers)
        if response.status_code != 200:
            logger.error(f"failed to get news: {response}")
            return

        html = response.text
        self._save(html, "news.html")

    def get_token(self):
        response = self._session.get(github.login_url, headers=github.headers)
        selector = etree.HTML(response.text)
        # 崔庆才的源代码中获取 token 的 xpath 已不适用，此处做了修改
        token = selector.xpath('//*[@id="login"]/div[4]/form/input[1]/@value')
        return token

    def _save(self, html: str, dest_path: str):
        with open(fs.log_dir / dest_path, "w", encoding="utf-8") as f:
            f.write(html)


if __name__ == "__main__":
    github_crawler = GithubCrawler()
    github_crawler.login()
    github_crawler.get_news()
