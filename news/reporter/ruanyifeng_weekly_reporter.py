from news.util import timelib
from news.util.logger import logger
from news.util.mongodb import mongo


def report():
    yesterday = timelib.yesterday()
    blogs = mongo.find(
        "ruanyifeng_weekly", {"crawled_at": {"$gte": yesterday}}, [("created_at", -1)]
    )
    logger.info(f"ruanyifeng weekly count: {len(blogs)}")
    if len(blogs) == 0:
        return ""

    content = ""
    for blog in blogs:
        content += get_blog(blog)

    return content


def get_blog(blog: dict):
    date = timelib.format_iso8601_time(blog["created_at"])
    content = f"## [{blog['id']}]({blog['url']})\n\n"
    content += f"> {date}\n\n"
    for name, news_list in blog["sections"].items():
        content += f"### {name}\n\n"
        content += "\n".join(news_list)
        content += "\n\n"
    return content


if __name__ == "__main__":
    report()
