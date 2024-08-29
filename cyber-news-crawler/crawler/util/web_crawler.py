from crawler.util import fs
from crawler.util import myrequests
from crawler.util.logger import logger
from crawler.util.mongodb import mongo
from crawler.util.web_parser import WebParser


class WebCrawler:
    def __init__(
        self,
        parser: WebParser,
        url: str,
        name: str,
        headers: dict = None,
        primary_key: str = "id",
    ):
        """
        Args:
            parser: 网页解析器
            url: 待爬取的 URL 地址
            name: 网页名字
            header: HTTP header
            primary_key: 数据保存在数据库时 primary_key 字段的名字
        """
        self._parser = parser
        self._url = url
        self._name = name
        self._headers = headers
        self._primary_key = primary_key

    def crawl(self) -> bool:
        response = myrequests.get(self._url, headers=self._headers, timeout=10)
        if response is None:
            logger.error(f"No response from {self._url}")
            return False

        if response.status_code != 200:
            logger.error(
                f"Failed to get webpage. Status Code: {response.status_code}, URL: {self._url}"
            )
            return False

        fs.save_response_text(response.text, self._name)
        news_list = self._parser.parse(response.text)
        mongo.insert_many_new(self._name, self._primary_key, news_list)
        return True
