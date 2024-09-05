from news.util import timelib
from news.util.logger import logger
from news.util.mongodb import mongo


def report():
    content = report_rust_blog()
    return content


def report_rust_blog():
    content = "## Rust Blog\n\n"
    yesterday = timelib.yesterday()
    last_month = timelib.n_days_ago(31)
    blog_list = mongo.find(
        "rust_blog",
        {"crawled_at": {"$gte": yesterday}, "created_at": {"$gte": last_month}},
        [("created_at", -1)],
    )
    logger.info(f"rust blog count: {len(blog_list)}")
    if len(blog_list) == 0:
        return ""

    for i, blog in enumerate(blog_list):
        content += get_blog(i, blog)

    content += "\n"
    return content


def get_blog(id: int, blog: dict):
    return f"{id+1}. [{blog['id']}]({blog['url']}) ({blog['created_at']})\n"
