from news.reporter import Reporter
from news.util.logger import logger
from news.util.mongodb import mongo
from news.util.timelib import n_hours_ago


class DailyNewsReporter(Reporter):
    def __init__(
        self,
        title: str,
        table_name: str = "",
        start_date: str = n_hours_ago(24),
        order_by: str = "crawled_at",
    ):
        """每日技术新闻记者
        :param title: 标题
        :param table_name: 数据库表的名字
        :param start_date: 设置待查询的新闻开始日期
        :param order_by: 新闻排序方式，默认按创建时间倒序排列
        """
        self._title = title
        self._start_date = start_date
        self._order_by = order_by

        if table_name == "":
            self._table_name = title.lower().replace(" ", "_")
        else:
            self._table_name = table_name

    def report(self) -> str:
        content = f"## {self._title}\n\n"
        news_list = mongo.find(
            self._table_name,
            {
                "crawled_at": {"$gte": self._start_date},
            },
            [(self._order_by, -1)],
        )
        logger.info(f"{self._title} count: {len(news_list)}")
        if len(news_list) == 0:
            return ""

        for i, news in enumerate(news_list):
            content += self._get_news(i, news)

        content += "\n"
        return content

    @staticmethod
    def _get_news(id: int, news: dict):
        return f"{id+1}. [{news['id']}]({news['url']}) ({news['created_at']})\n"
