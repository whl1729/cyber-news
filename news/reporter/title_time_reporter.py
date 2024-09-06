from news.util import timelib
from news.util.logger import logger
from news.util.mongodb import mongo


def report(title: str, table_name: str = ""):
    """新闻报告
    :param title: 标题
    :param table_name: 数据库表的名字
    """
    content = f"## {title}\n\n"
    if table_name == "":
        table_name = title.lower().replace(" ", "_")
    yesterday = timelib.yesterday()
    news_list = mongo.find(
        table_name,
        {"created_at": {"$gte": yesterday}},
        [("created_at", -1)],
    )
    logger.info(f"{title} count: {len(news_list)}")
    if len(news_list) == 0:
        return ""

    for i, news in enumerate(news_list):
        content += get_news(i, news)

    content += "\n"
    return content


def get_news(id: int, news: dict):
    return f"{id+1}. [{news['id']}]({news['url']}) ({news['created_at']})\n"
