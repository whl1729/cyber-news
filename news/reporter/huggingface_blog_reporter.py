from news.reporter.daily_news_reporter import DailyNewsReporter


class HuggingfaceBlogReporter(DailyNewsReporter):
    def __init__(self):
        super().__init__(
            title="Hugging Face Blog",
            table_name="huggingface_blog",
            order_by="created_at",
        )


def report() -> str:
    reporter = HuggingfaceBlogReporter()
    return reporter.report()


if __name__ == "__main__":
    print(report())
