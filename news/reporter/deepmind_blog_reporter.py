from news.reporter.daily_news_reporter import DailyNewsReporter


class DeepmindBlogReporter(DailyNewsReporter):
    def __init__(self):
        super().__init__(
            title="DeepMind Blog",
            table_name="deepmind_blog",
            order_by="created_at",
        )


def report() -> str:
    reporter = DeepmindBlogReporter()
    return reporter.report()


if __name__ == "__main__":
    print(report())
