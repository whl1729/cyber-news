from crawler.util import fs
from crawler.util import myrequests
from crawler.util.logger import logger
from crawler.util.mongodb import mongo
from crawler.util.web_parser import WebParser


def crawl(
    parser: WebParser,
    url: str,
    name: str,
    headers: dict = None,
    proxies: dict = None,
) -> bool:
    response = myrequests.get(url, headers=headers, proxies=proxies, timeout=10)
    if response is None:
        logger.error(f"No response from {url}")
        return False

    if response.status_code != 200:
        logger.error(
            f"Failed to get webpage. Status Code: {response.status_code}, URL: {url}"
        )
        return False

    fs.save_response_text(response.text, name)
    news_list = parser.parse(response.text)
    count = mongo.insert_many_new(name, "id", news_list)
    logger.info(f"{count} {name.replace('_', ' ')} inserted")
    return True
