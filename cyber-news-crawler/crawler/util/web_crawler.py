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
    resp_text = get(url, name=name, headers=headers, proxies=proxies)
    if resp_text == "":
        return False

    try:
        news_list = parser.parse(resp_text)
    except Exception as e:
        logger.error(f"{parser} failed to parse {name}: {e}")
        return False

    count = mongo.insert_many_new(name, "id", news_list)
    logger.info(f"{count} {name.replace('_', ' ')} inserted")
    return True


def get(
    url: str,
    name: str,
    headers: dict = None,
    proxies: dict = None,
) -> str:
    response = myrequests.get(url, headers=headers, proxies=proxies, timeout=10)
    response.encoding = "utf-8"
    if response is None:
        logger.error(f"No response from {url}")
        return ""

    if response.status_code != 200:
        logger.error(
            f"Failed to get webpage. Status Code: {response.status_code}, URL: {url}"
        )
        return ""

    fs.save_response_text(response.text, name)
    return response.text
