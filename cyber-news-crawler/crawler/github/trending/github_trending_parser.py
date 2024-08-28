from bs4 import BeautifulSoup
from crawler import github
from crawler.util import timelib
from crawler.util.logger import logger
from crawler.util.mongodb import mongo


class GithubTrendingParser:
    def parse(self, resp_text: str):
        soup = BeautifulSoup(resp_text, "html.parser")

        articles = soup.find_all("article", {"class": "Box-row"})
        repos = [GithubRepository(article).parse() for article in articles]
        logger.info(f"Successfully crawled {len(repos)} github trending repos")

        for repo in repos:
            if repo is None:
                continue

            exists = mongo.find("github_trending", {"name": repo["name"]})
            if not exists:
                mongo.insert_one("github_trending", repo)
                logger.info(f"Successfully inserted a github trending repo: {repo}")

        return repos


class GithubRepository:
    def __init__(self, article):
        self._article = article

    def parse(self):
        """提取 Github 仓库的信息"""
        name = self._parse_name()
        if name == "":
            return None

        link = self._parse_link()
        description = self._parse_desc()
        language = self._parse_language()
        stars = self._parse_stars()
        forks = self._parse_forks()
        stars_today = self._parse_stars_today()
        now = timelib.now2()

        return {
            "name": name,
            "link": link,
            "description": description,
            "language": language,
            "stars": stars,
            "forks": forks,
            "stars_today": stars_today,
            "time": now,
        }

    def _parse_name(self):
        try:
            return self._article.h2.a.text.strip().replace("\n", "").replace(" ", "")
        except Exception as e:
            logger.error(f"Failed to parse repo name: {e}")
            return ""

    def _parse_link(self):
        try:
            return github.host + self._article.h2.a["href"]
        except Exception as e:
            logger.error(f"Failed to parse repo link: {e}")
            return ""

    def _parse_desc(self):
        try:
            return self._article.p.text.strip() if self._article.p else "No description"
        except Exception as e:
            logger.error(f"Failed to parse repo desc: {e}")
            return ""

    def _parse_language(self):
        target = self._article.find("span", {"itemprop": "programmingLanguage"})
        return target.text.strip() if target else "Not specified"

    def _parse_stars(self):
        target = self._article.find(
            "a", {"href": self._article.h2.a["href"] + "/stargazers"}
        )
        stars = target.text.strip().replace(",", "") if target else -1
        try:
            return int(stars)
        except Exception:
            logger.error(f"Failed to transform stars to int: '{stars}'")
            return -1

    def _parse_forks(self):
        target = self._article.find(
            "a", {"href": self._article.h2.a["href"] + "/forks"}
        )
        forks = target.text.strip().replace(",", "") if target else -1
        try:
            return int(forks)
        except Exception:
            logger.error(f"Failed to transform forks to int: '{forks}'")

    def _parse_stars_today(self):
        target = self._article.find("span", {"class": "d-inline-block float-sm-right"})
        stars_today = target.text.strip().split()[0].replace(",", "") if target else -1
        try:
            return int(stars_today)
        except Exception:
            logger.error(f"Failed to transform stars_today to int: '{stars_today}'")
            return -1
