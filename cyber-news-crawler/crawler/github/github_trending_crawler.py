from bs4 import BeautifulSoup
from crawler import github
from crawler.util import timelib
from crawler.util import web_crawler
from crawler.util.configer import config
from crawler.util.logger import logger


class GithubTrendingParser:
    def parse(self, resp_text: str):
        soup = BeautifulSoup(resp_text, "html.parser")
        articles = soup.find_all("article", {"class": "Box-row"})
        trendings = []
        for article in articles:
            trending = self._parse_article(article)
            if trending:
                trendings.append(trending)

        logger.info(f"{len(trendings)} github trendings parsed")
        return trendings

    def _parse_article(self, article: str) -> dict:
        """提取 Github 仓库的信息"""
        name = self._parse_name(article)
        if name == "":
            return {}

        link = self._parse_link(article)
        description = self._parse_desc(article)
        language = self._parse_language(article)
        stars = self._parse_stars(article)
        forks = self._parse_forks(article)
        stars_today = self._parse_stars_today(article)
        now = timelib.now2()

        return {
            "id": name,
            "link": link,
            "description": description,
            "language": language,
            "stars": stars,
            "forks": forks,
            "stars_today": stars_today,
            "time": now,
        }

    @staticmethod
    def _parse_name(article: str):
        try:
            return article.h2.a.text.strip().replace("\n", "").replace(" ", "")
        except Exception as e:
            logger.error(f"Failed to parse repo name: {e}")
            return ""

    @staticmethod
    def _parse_link(article: str):
        try:
            return github.host + article.h2.a["href"]
        except Exception as e:
            logger.error(f"Failed to parse repo link: {e}")
            return ""

    @staticmethod
    def _parse_desc(article: str):
        try:
            return article.p.text.strip() if article.p else "No description"
        except Exception as e:
            logger.error(f"Failed to parse repo desc: {e}")
            return ""

    @staticmethod
    def _parse_language(article: str):
        target = article.find("span", {"itemprop": "programmingLanguage"})
        return target.text.strip() if target else "Not specified"

    @staticmethod
    def _parse_stars(article: str):
        target = article.find("a", {"href": article.h2.a["href"] + "/stargazers"})
        stars = target.text.strip().replace(",", "") if target else -1
        try:
            return int(stars)
        except Exception:
            logger.error(f"Failed to transform stars to int: '{stars}'")
            return -1

    @staticmethod
    def _parse_forks(article: str):
        target = article.find("a", {"href": article.h2.a["href"] + "/forks"})
        forks = target.text.strip().replace(",", "") if target else -1
        try:
            return int(forks)
        except Exception:
            logger.error(f"Failed to transform forks to int: '{forks}'")

    @staticmethod
    def _parse_stars_today(article: str):
        target = article.find("span", {"class": "d-inline-block float-sm-right"})
        stars_today = target.text.strip().split()[0].replace(",", "") if target else -1
        try:
            return int(stars_today)
        except Exception:
            logger.error(f"Failed to transform stars_today to int: '{stars_today}'")
            return -1


def crawl():
    parser = GithubTrendingParser()
    web_crawler.crawl(
        parser,
        github.trending_url,
        "github_trending",
        proxies=config["proxies"],
    )


if __name__ == "__main__":
    crawl()
