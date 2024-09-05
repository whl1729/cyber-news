from news.reporter import cpp_reporter
from news.reporter import github_notification_reporter
from news.reporter import github_received_event_reporter
from news.reporter import github_trending_reporter
from news.reporter import go_reporter
from news.reporter import hacker_news_reporter
from news.reporter import new_stack_reporter
from news.reporter import python_reporter
from news.reporter import ruanyifeng_weekly_reporter
from news.reporter import rust_reporter
from news.util import fs
from news.util import timelib


def report():
    content = create_header()
    content += cpp_reporter.report()
    content += go_reporter.report()
    content += python_reporter.report()
    content += rust_reporter.report()
    content += ruanyifeng_weekly_reporter.report()
    content += github_trending_reporter.report()
    content += new_stack_reporter.report()
    content += hacker_news_reporter.report()
    content += github_received_event_reporter.report()
    content += github_notification_reporter.report()
    filename = f"{timelib.today()}.md"
    fs.save_post(content, filename)


def create_header():
    delimiter = "+++"
    title = f'title = "{timelib.today2()}的新闻"'
    date = f"date = {timelib.now4()}"
    return f"{delimiter}\n{title}\n{date}\n{delimiter}\n<!--more-->\n"


if __name__ == "__main__":
    report()
