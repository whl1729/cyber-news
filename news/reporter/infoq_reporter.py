from news.util import timelib
from news.util.logger import logger
from news.util.mongodb import mongo


def report():
    content = "## InfoQ\n\n"
    yesterday = timelib.yesterday()
    blog_list = mongo.find(
        "infoq",
        {"created_at": {"$gte": yesterday}},
        [("created_at", -1)],
    )
    logger.info(f"infoq blog count: {len(blog_list)}")
    if len(blog_list) == 0:
        return ""

    for i, blog in enumerate(blog_list):
        content += get_go_blog(i, blog)

    return content


def get_go_blog(id: int, blog: dict):
    content = f"{id+1}. [{blog['id']}]({blog['url']})\n"
    content += f"  - Author: {blog['author']}; Time: {blog['created_at']}\n\n"
    return content
