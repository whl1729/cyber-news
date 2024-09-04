from news.util import timelib
from news.util.logger import logger
from news.util.mongodb import mongo

TITLE = "## Github Received Events\n\n"


def report():
    today = timelib.today()
    event_list = mongo.find("github_received_events", {"created_at": {"$gte": today}})
    logger.info(f"github received events count: {len(event_list)}")
    if len(event_list) == 0:
        return ""

    content = TITLE
    for i, event in enumerate(event_list):
        content += get_event(i, event)

    return content


def get_event(id: int, event: dict):
    do = get_action(event["type"])
    when = timelib.format_iso_time(event["created_at"])
    content = f"{id+1}. [{event['actor_name']}]({event['actor_url']}) {do} [{event['repo_name']}]({event['repo_url']}) at {when}\n\n"
    return content


def get_action(event_type: str) -> str:
    translation = {
        "CreateEvent": "creates",
        "ForkEvent": "forks",
        "MemberEvent": "adds or removes",
        "PublicEvent": "publicizes",
        "WatchEvent": "stars",
    }

    return translation.get(event_type, event_type)
