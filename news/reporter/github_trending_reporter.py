from news.util import timelib
from news.util.logger import logger
from news.util.mongodb import mongo

TITLE = "## Github Trending\n\n"


def report():
    today = timelib.today()
    news_list = mongo.find(
        "github_trending", {"time": {"$gte": today}}, [("stars_today", -1)]
    )
    logger.info(f"github trending news count: {len(news_list)}")
    if len(news_list) == 0:
        return ""

    content = TITLE
    for i, news in enumerate(news_list):
        content += get_news(i, news)

    content += "\n"
    return content


def get_news(id: int, news: dict):
    return f"{id+1}. [{news['id']}]({news['link']}): {news['description']}\n"
