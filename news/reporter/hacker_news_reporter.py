from news.util import timelib
from news.util.logger import logger
from news.util.mongodb import mongo

TITLE = "## Hacker News\n\n"


def report():
    today = timelib.today()
    news_list = mongo.find(
        "hacker_news", {"updated_at": {"$gte": today}}, [("score", -1)]
    )
    logger.info(f"hacker news count: {len(news_list)}")
    if len(news_list) == 0:
        return ""

    content = TITLE
    for i, news in enumerate(news_list):
        content += get_news(i, news)

    return content


def get_news(id: int, news: dict):
    content = f"{id+1}. [{news['title']}]({news['url']})"
    content += f" ([{news['host']}](https://{news['host']}))\n"
    content += f"  - Time: {timelib.format_iso8601_time_2(news['created_at'])};"
    content += f" Points: {news['score']}; Comments: {news['comment_count']}\n\n"
    return content
