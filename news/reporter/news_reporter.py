from news.reporter import github_notification_reporter
from news.reporter import github_received_event_reporter
from news.reporter import github_trending_reporter
from news.reporter import ruanyifeng_weekly_reporter
from news.util import fs
from news.util import timelib
from news.util.logger import logger
from news.util.mongodb import mongo
from news.util.timelib import yesterday


def report():
    title_and_table_names = [
        ("机器之心", "jiqizhixin"),
        ("量子位", "liangziwei"),
        ("新智元", "xinzhiyuan"),
        ("极客公园", "geekpark"),
        ("C++ Blog", "isocpp_blog"),
        ("Go Blog", "go_blog"),
        ("Go News", "go_news"),
        ("Python Insider", "python_insider"),
        ("Rust Blog", "rust_blog"),
        ("The New Stack", "new_stack"),
        ("InfoQ", "infoq"),
        ("Hacker News", "hacker_news"),
    ]

    content = create_header()
    for title, table_name in title_and_table_names:
        content += report_news(title, table_name)

    content += github_trending_reporter.report()
    content += ruanyifeng_weekly_reporter.report()
    content += github_received_event_reporter.report()
    content += github_notification_reporter.report()
    filename = f"{timelib.today()}.md"
    fs.save_post(content, filename)


def create_header():
    delimiter = "+++"
    title = f'title = "{timelib.today2()}的新闻"'
    date = f"date = {timelib.now4()}"
    return f"{delimiter}\n{title}\n{date}\n{delimiter}\n<!--more-->\n"


def report_news(title: str, table_name: str = "", start_date: str = yesterday()):
    """新闻报告
    :param title: 标题
    :param table_name: 数据库表的名字
    :param start_date: 设置待查询的新闻开始日期
    """
    content = f"## {title}\n\n"
    if table_name == "":
        table_name = title.lower().replace(" ", "_")
    news_list = mongo.find(
        table_name,
        {"crawled_at": {"$gte": yesterday()}, "created_at": {"$gte": start_date}},
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


if __name__ == "__main__":
    report()
