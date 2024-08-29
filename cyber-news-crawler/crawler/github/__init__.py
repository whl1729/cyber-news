from crawler.util.configer import config

host = "https://github.com"
notification_url = "https://api.github.com/notifications"
received_event_url = (
    f'https://api.github.com/users/{config["github_username"]}/received_events'
)
trending_url = "https://github.com/trending"

headers = {
    "Authorization": f'token {config["github_token"]}',
    "Accept": "application/vnd.github.v3+json",
}
