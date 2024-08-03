from dataclasses import dataclass

from crawler.github import url_prefix
from crawler.util.logger import logger
from crawler.util.mylist import first
from crawler.util.mylist import strip_join
from lxml import etree


@dataclass
class Activity:
    who: str
    do: str
    what: str
    when: str
    abstract: str
    link: str


feed_xpaths = {
    "title": [
        "div/div/div/div[1]/div/div",
        "div/div/div/div[1]/div",
        "div/div/div/div[1]",
    ],
    "do": [
        "text()",
        "span[2]/text()",
    ],
    "what": [
        "a[2]/text()",
        "span[2]/span[1]/text()",
    ],
    "when": [
        "span[2]/relative-time/@datetime",
        "span[2]/span/relative-time/@datetime",
        "span[2]/span[2]/relative-time/@datetime",
    ],
    "abstract": [
        "div/div/div/div[2]/div/div[2]/p/text()",
        "div/div/div/div[2]/div/div/div/div/text()",
        "div/div/div/div[2]/div/div/div/div/div/div/div[2]/p/text()",
        "div/div/div/div[2]/div/div/div/div/div/div/div/div/div/text()",
    ],
    "link": [
        "div/div/div/div[2]/div/div[1]/a/@href",
        "div/div/div/div[2]/div/div[1]/div[1]/div/a/@href",
        "div/div/div/div[2]/div/div/span/span[1]/a[1]/@href",
        "div/div/div/div[2]/div/div/div/div/div/div/div[1]/a/@href",
        "div/div/div/div[2]/div/div/div/div/div/div/div/span/span[1]/a[1]/@href",
    ],
}


class GithubFeedParser:
    """Parse Github dashboard-feed page"""

    def __init__(self):
        pass

    def parse(self, text: str):
        selector = etree.HTML(text)
        activities = []
        divs = selector.xpath("/html/body/div[1]/div[5]/main/div/div")
        for div in divs:
            activity = self._parse_activity(div)
            if activity is not None:
                activities.append(activity)
        return activities

    def _parse_activity(self, div):
        title = self._parse_element(div, "title", None)
        if title is None:
            logger.error(f"failed to get activity title: {div}")
            return None

        who = first(title.xpath("a[1]/text()"))
        do = self._parse_do(title)
        what = self._parse_element(title, "what").strip()
        when = self._parse_element(title, "when")
        abstract = self._parse_element(div, "abstract").strip()
        link = url_prefix + self._parse_element(div, "link")

        activity = Activity(
            who=who,
            do=do,
            what=what,
            when=when,
            abstract=abstract,
            link=link,
        )
        logger.info(f"activity: {activity}")
        return activity

    def _parse_element(self, div, elem_type: str, default=""):
        paths = feed_xpaths.get(elem_type, [])
        for path in paths:
            data = first(div.xpath(path))
            if len(data) > 0:
                return data
        return default

    def _parse_do(self, div):
        paths = feed_xpaths["do"]
        for path in paths:
            data = strip_join(div.xpath(path))
            if len(data) > 0:
                return data
        return ""
