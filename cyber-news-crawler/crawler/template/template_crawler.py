from crawler.template.template_parser import TemplateParser
from crawler.util import fs
from crawler.util import myrequests
from crawler.util.logger import logger
from crawler.util.mongodb import mongo

url = ""


class TemplateCrawler:
    def __init__(self):
        self._parser = TemplateParser()

    def crawl(self):
        response = myrequests.get(url, timeout=10)
        if response is None:
            logger.error(f"Failed to get the webpage: {url}")
            return None

        fs.save_log(response.text, "template.html")
        news_list = self._parser.parse(response.text)
        mongo.insert_many_new("template", "id", news_list)


if __name__ == "__main__":
    crawler = TemplateCrawler()
    crawler.crawl()
