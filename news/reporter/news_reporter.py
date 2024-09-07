from news.reporter import github_notification_reporter
from news.reporter import github_received_event_reporter
from news.reporter import github_trending_reporter
from news.reporter import ruanyifeng_weekly_reporter
from news.reporter.daily_news_reporter import DailyNewsReporter
from news.reporter.weekly_news_reporter import WeeklyNewsReporter
from news.util import fs
from news.util import timelib


def report():
    content = create_header()
    content += report_daily_news()
    content += report_weekly_news()
    content += report_personal_news()

    filename = f"{timelib.today()}.md"
    fs.save_post(content, filename)


def create_header():
    delimiter = "+++"
    title = f'title = "{timelib.today2()}的新闻"'
    date = f"date = {timelib.now4()}"
    return f"{delimiter}\n{title}\n{date}\n{delimiter}\n<!--more-->\n"


def report_daily_news() -> str:
    """报道每日新闻"""
    daily_reporters = [
        DailyNewsReporter("机器之心", "jiqizhixin"),
        DailyNewsReporter("量子位", "liangziwei"),
        DailyNewsReporter("新智元", "xinzhiyuan"),
        DailyNewsReporter("极客公园", "geekpark"),
        DailyNewsReporter("C++ Blog", "isocpp_blog"),
        DailyNewsReporter("Go Blog"),
        DailyNewsReporter("Go News"),
        DailyNewsReporter("Python Insider"),
        DailyNewsReporter("Rust Blog"),
        DailyNewsReporter("New Stack"),
        DailyNewsReporter("InfoQ"),
        DailyNewsReporter("Hacker News"),
    ]

    content = ""
    for reporter in daily_reporters:
        content += reporter.report()

    content += github_trending_reporter.report()
    return content


def report_weekly_news() -> str:
    """报道周刊"""
    weekly_reporters = [
        WeeklyNewsReporter("Go Weekly"),
        WeeklyNewsReporter("Rust Weekly"),
    ]

    content = ruanyifeng_weekly_reporter.report()
    for reporter in weekly_reporters:
        content += reporter.report()

    return content


def report_personal_news() -> str:
    """报道私人化的新闻"""
    content = github_received_event_reporter.report()
    content += github_notification_reporter.report()
    return content


if __name__ == "__main__":
    report()
