import traceback

from news.util import fs
from news.util import myrequests
from news.util.logger import logger
from news.util.mongodb import mongo
from news.util.web_parser import WebParser


def crawl(
    parser: WebParser,
    url: str,
    name: str,
    headers: dict = None,
    proxies: dict = None,
    use_selenium: bool = False,
) -> bool:
    resp_text = get(
        url, name=name, headers=headers, proxies=proxies, use_selenium=use_selenium
    )
    if resp_text == "":
        return False

    try:
        news_list = parser.parse(resp_text)
    except Exception as e:
        logger.error(
            f"{parser} failed to parse {name}: {e}, trace: {traceback.format_exc()}"
        )
        return False

    count = mongo.insert_many_new(name, "id", news_list)
    logger.info(f"{count} {name.replace('_', ' ')} inserted")
    return True


def get(
    url: str,
    name: str,
    headers: dict = None,
    proxies: dict = None,
    use_selenium: bool = False,
) -> str:
    if use_selenium:
        response = myrequests.get_with_selenium(url, timeout=10)
    else:
        response = myrequests.get(url, headers=headers, proxies=proxies, timeout=10)

    if response is None:
        logger.error(f"No response from {url}")
        return ""

    if response.status_code != 200:
        logger.error(
            f"Failed to get webpage. Status Code: {response.status_code}, URL: {url}"
        )
        return ""

    response.encoding = "utf-8"
    fs.save_response_text(response.text, name)
    return response.text
