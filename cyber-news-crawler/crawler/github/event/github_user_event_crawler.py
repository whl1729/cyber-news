from crawler.github.event.github_user_event_parser import GithubUserEventParser
from crawler.util import fs
from crawler.util import myrequests
from crawler.util.configer import config
from crawler.util.logger import logger
from crawler.util.mongodb import mongo

# 获取你关注的用户的活动
url = f'https://api.github.com/users/{config["github_username"]}/received_events'


class GithubUserEventCrawler:
    def __init__(self):
        self._parser = GithubUserEventParser()
        self._headers = {"Authorization": config["github_token"]}

    def crawl(self):
        response = myrequests.get(url, headers=self._headers, timeout=10)
        if response is None:
            logger.error(f"Failed to get the webpage: {url}")
            return None

        fs.save_json(response.text, "github_user_events.json")
        events = self._parser.parse(response.text)
        logger.info(f"Github received events count: {len(events)}")
        for event in events:
            logger.debug(f"event: {event.to_json()}")

        documents = [event.to_json() for event in events]
        inserted_count = mongo.insert_many_new(
            "github_received_events", "id", documents
        )
        logger.info(f"Github received events inserted count: {inserted_count}")


if __name__ == "__main__":
    crawler = GithubUserEventCrawler()
    crawler.crawl()
