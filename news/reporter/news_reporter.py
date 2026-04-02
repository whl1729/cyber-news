from news.reporter import github_notification_reporter
from news.reporter import github_received_event_reporter
from news.reporter import github_trending_reporter
from news.reporter import ruanyifeng_weekly_reporter
from news.reporter.crawler_health_reporter import CrawlerHealthReporter
from news.reporter.daily_news_reporter import DailyNewsReporter
from news.reporter.weekly_news_reporter import WeeklyNewsReporter
from news.util import fs
from news.util import timelib


def report():
    content = create_header()
    content += report_daily_news()
    # content += report_weekly_news()
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
        DailyNewsReporter(
            "Claude Code Blog", "claude_code_blog", order_by="created_at"
        ),
        DailyNewsReporter("OpenAI News", "openai_news", order_by="created_at"),
        DailyNewsReporter("DeepMind Blog", "deepmind_blog", order_by="created_at"),
        DailyNewsReporter(
            "Hugging Face Blog", "huggingface_blog", order_by="created_at"
        ),
        DailyNewsReporter("Karpathy Blog", "karpathy_blog", order_by="created_at"),
        DailyNewsReporter("Chip Huyen Blog", "chip_huyen_blog", order_by="created_at"),
        DailyNewsReporter(
            "Sebastian Raschka Blog", "sebastian_raschka_blog", order_by="created_at"
        ),
        DailyNewsReporter(
            "Simon Willison Blog", "simon_willison_blog", order_by="created_at"
        ),
        DailyNewsReporter(
            "Harrison Chase Blog", "harrison_chase_blog", order_by="created_at"
        ),
        DailyNewsReporter(
            "Yohei Nakajima Blog", "yohei_nakajima_blog", order_by="created_at"
        ),
        DailyNewsReporter("BaoYu Blog", "baoyu_blog", order_by="created_at"),
        DailyNewsReporter("Sam Altman Blog", "sam_altman_blog", order_by="created_at"),
        DailyNewsReporter(
            "Mario Zechner Blog", "mario_zechner_blog", order_by="created_at"
        ),
        DailyNewsReporter("DHH Blog", "dhh_blog", order_by="created_at"),
        DailyNewsReporter(
            "Armin Ronacher Blog", "armin_ronacher_blog", order_by="created_at"
        ),
        DailyNewsReporter("antirez Blog", "antirez_blog", order_by="created_at"),
        DailyNewsReporter("Ryan Dahl Blog", "ryan_dahl_blog", order_by="created_at"),
        DailyNewsReporter(
            "The Pragmatic Engineer", "pragmatic_engineer_blog", order_by="created_at"
        ),
        DailyNewsReporter(
            "sean goedecke Blog", "sean_goedecke_blog", order_by="created_at"
        ),
        DailyNewsReporter(
            "Philipp Schmid Blog", "philipp_schmid_blog", order_by="created_at"
        ),
        DailyNewsReporter(
            "Matt Shumer Blog", "matt_shumer_blog", order_by="created_at"
        ),
        DailyNewsReporter(
            "Bassim Eledath Blog", "bassim_eledath_blog", order_by="created_at"
        ),
        DailyNewsReporter("Rob Zolkos Blog", "rob_zolkos_blog", order_by="created_at"),
        DailyNewsReporter(
            "Chris Gregori Blog", "chris_gregori_blog", order_by="created_at"
        ),
        DailyNewsReporter(
            "Addy Osmani Blog", "addy_osmani_blog", order_by="created_at"
        ),
        DailyNewsReporter(
            "Uwe Friedrichsen Blog", "uwe_friedrichsen_blog", order_by="created_at"
        ),
        DailyNewsReporter(
            "One Useful Thing", "one_useful_thing_blog", order_by="created_at"
        ),
        DailyNewsReporter("Han, Not Solo", "han_not_solo_blog", order_by="created_at"),
        DailyNewsReporter("量子位", "liangziwei"),
        DailyNewsReporter("C++ Blog", "isocpp_blog"),
        DailyNewsReporter("Go Blog"),
        DailyNewsReporter("Go News"),
        DailyNewsReporter("Python Insider"),
        DailyNewsReporter("Rust Blog"),
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
        WeeklyNewsReporter("Pycoder Weekly"),
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


def report_crawler_health() -> str:
    """报道爬虫健康状态"""
    reporter = CrawlerHealthReporter()
    content = "\n\n---\n\n"
    content += reporter.generate_daily_report()
    return content


if __name__ == "__main__":
    report()
