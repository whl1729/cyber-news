from bs4 import BeautifulSoup
from crawler import github
from crawler.util import fs
from crawler.util import myrequests
from crawler.util.logger import logger


class GithubTrendingCrawler:
    def crawl(self):
        response = myrequests.get(github.trending_url)
        if response is None:
            logger.error("Failed to retrieve the github trending page")
            return None

        fs.save_log(response.text, "github_trending.html")
        soup = BeautifulSoup(response.text, "html.parser")

        articles = soup.find_all("article", {"class": "Box-row"})
        repos = [GithubRepository(article).parse() for article in articles]

        # 打印仓库信息
        for repo in repos:
            if repo is None:
                continue

            logger.info(f"Name: {repo['name']}")
            logger.info(f"Link: {repo['link']}")
            logger.info(f"Description: {repo['description']}")
            logger.info(f"Language: {repo['language']}")
            logger.info(f"Stars: {repo['stars']}")
            logger.info(f"Forks: {repo['forks']}")
            logger.info(f"Stars Today: {repo['stars_today']}")
            logger.info("=" * 100)

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

        return {
            "name": name,
            "link": link,
            "description": description,
            "language": language,
            "stars": stars,
            "forks": forks,
            "stars_today": stars_today,
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


if __name__ == "__main__":
    trending_crawler = GithubTrendingCrawler()
    trending_crawler.crawl()
