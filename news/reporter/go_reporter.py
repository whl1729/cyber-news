from news.util import timelib
from news.util.logger import logger
from news.util.mongodb import mongo

TITLE = "## Go\n\n"


def report():
    content = report_go_blog()
    if content == "":
        return ""
    return TITLE + content


def report_go_blog():
    content = "### Go Blog\n\n"
    yesterday = timelib.yesterday()
    last_month = timelib.n_days_ago(31)
    blog_list = mongo.find(
        "go_blog",
        {"crawled_at": {"$gte": yesterday}, "created_at": {"$gte": last_month}},
        [("created_at", -1)],
    )
    logger.info(f"go blog count: {len(blog_list)}")
    if len(blog_list) == 0:
        return ""

    for i, blog in enumerate(blog_list):
        content += get_blog(i, blog)

    return content


def get_blog(id: int, blog: dict):
    content = f"{id+1}. [{blog['id']}]({blog['url']})\n"
    content += f"  - {blog['summary']}\n"
    content += f"  - Author: {blog['author']}; Time: {blog['created_at']}\n\n"
    return content
