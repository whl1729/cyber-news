from news.reporter import Reporter
from news.util.logger import logger
from news.util.mongodb import mongo
from news.util.timelib import n_days_ago


class WeeklyNewsReporter(Reporter):
    def __init__(self, title: str, table_name: str = ""):
        """每周技术新闻记者
        :param title: 标题
        :param table_name: 数据库表的名字
        :param start_date: 设置待查询的新闻开始日期
        """
        self._title = title

        if table_name == "":
            self._table_name = title.lower().replace(" ", "_")
        else:
            self._table_name = table_name

    def report(self) -> str:
        weekly = mongo.find_one(
            self._table_name,
            {"created_at": {"$gte": n_days_ago(7)}},
            [("created_at", -1)],
        )
        if not weekly:
            return ""

        logger.info(f"{self._title} blogs count: {len(weekly['blogs'])}")

        content = f"## [{weekly['id']}]({weekly['url']})\n\n"
        content += f"> {weekly['created_at']}\n\n"
        for i, blog in enumerate(weekly["blogs"]):
            content += self._get_blog(i, blog)

        content += "\n"
        return content

    @staticmethod
    def _get_blog(id: int, blog: dict):
        return f"{id+1}. [{blog['title']}]({blog['url']})\n"
