from news.reporter.daily_news_reporter import DailyNewsReporter


class YoheiNakajimaBlogReporter(DailyNewsReporter):
    def __init__(self):
        super().__init__(
            title="Yohei Nakajima Blog",
            table_name="yohei_nakajima_blog",
            order_by="created_at",
        )


def report() -> str:
    reporter = YoheiNakajimaBlogReporter()
    return reporter.report()


if __name__ == "__main__":
    print(report())
