from crawler import github
from crawler.github.trending.github_trending_parser import GithubTrendingParser
from crawler.util import fs
from crawler.util import myrequests
from crawler.util.configer import config
from crawler.util.logger import logger


class GithubTrendingCrawler:
    def __init__(self):
        self._parser = GithubTrendingParser()

    def crawl(self):
        response = myrequests.get(
            github.trending_url, proxies=config["proxies"], timeout=10
        )
        if response is None:
            logger.error("Failed to retrieve the github trending page")
            return None

        fs.save_response_text(response.text, "github_trending.html")
        return self._parser.parse(response.text)


if __name__ == "__main__":
    trending_crawler = GithubTrendingCrawler()
    trending_crawler.crawl()
