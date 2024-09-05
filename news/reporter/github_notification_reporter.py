from news.util import timelib
from news.util.logger import logger
from news.util.mongodb import mongo

TITLE = "## Github Notifications\n\n"


def report():
    today = timelib.today()
    notification_list = mongo.find(
        "github_notifications", {"updated_at": {"$gte": today}}
    )
    logger.info(f"github notifications count: {len(notification_list)}")
    if len(notification_list) == 0:
        return ""

    content = TITLE
    for i, notification in enumerate(notification_list):
        content += get_notification(i, notification)

    return content


def get_notification(id: int, notification: dict):
    article = get_article(notification["type"])
    when = timelib.format_iso_time(notification["updated_at"])
    content = f"{id+1}. {article} {notification['type']} on **{notification['repo']}**: [{notification['subject']}]({notification['url']}) ({when})\n\n"
    return content


def get_article(notification_type: str):
    """获取冠词"""
    vowels = ["A", "E", "I", "O", "U"]
    return "An" if notification_type.upper()[0] in vowels else "A"
