from datetime import datetime
from datetime import timedelta
from typing import Dict
from typing import List

from news.util.mongodb import mongo


class CrawlerHealthReporter:
    """爬虫健康报告生成器"""

    def generate_daily_report(self, date: datetime = None) -> str:
        """生成每日健康报告"""
        if date is None:
            date = datetime.now()

        start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timedelta(days=1)

        # 查询当天的健康记录
        records = mongo.find(
            "crawler_health",
            filter={"timestamp": {"$gte": start_of_day, "$lt": end_of_day}},
            sorter=[("timestamp", -1)],
        )

        if not records:
            return f"# 爬虫健康报告 - {date.strftime('%Y-%m-%d')}\n\n无健康记录\n"

        # 统计数据
        stats = self._calculate_stats(records)

        # 生成报告
        report = self._format_daily_report(date, stats, records)
        return report

    def _calculate_stats(self, records: List[dict]) -> Dict:
        """计算统计数据"""
        stats = {}
        for record in records:
            crawler_name = record["crawler_name"]
            if crawler_name not in stats:
                stats[crawler_name] = {
                    "total": 0,
                    "success": 0,
                    "failed": 0,
                    "failure_reasons": {},
                }

            stats[crawler_name]["total"] += 1
            if record["success"]:
                stats[crawler_name]["success"] += 1
            else:
                stats[crawler_name]["failed"] += 1
                reason = record.get("failure_reason", "未知")
                stats[crawler_name]["failure_reasons"][reason] = (
                    stats[crawler_name]["failure_reasons"].get(reason, 0) + 1
                )

        return stats

    def _format_daily_report(
        self, date: datetime, stats: Dict, records: List[dict]
    ) -> str:
        """格式化每日报告"""
        report = f"# 爬虫健康报告 - {date.strftime('%Y-%m-%d')}\n\n"
        report += f"**总执行次数**: {len(records)}\n\n"

        # 按爬虫统计
        report += "## 爬虫统计\n\n"
        report += "| 爬虫名称 | 总次数 | 成功 | 失败 | 成功率 |\n"
        report += "|---------|--------|------|------|--------|\n"

        for crawler_name, stat in sorted(stats.items()):
            success_rate = (
                (stat["success"] / stat["total"] * 100) if stat["total"] > 0 else 0
            )
            report += f"| {crawler_name} | {stat['total']} | {stat['success']} | {stat['failed']} | {success_rate:.1f}% |\n"

        # 失败原因统计
        report += "\n## 失败原因统计\n\n"
        for crawler_name, stat in sorted(stats.items()):
            if stat["failed"] > 0:
                report += f"### {crawler_name}\n\n"
                for reason, count in sorted(
                    stat["failure_reasons"].items(), key=lambda x: x[1], reverse=True
                ):
                    report += f"- {reason}: {count} 次\n"
                report += "\n"

        return report

    def generate_trend_report(self, days: int = 30) -> str:
        """生成历史健康趋势报告（最近 N 天）"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        records = mongo.find(
            "crawler_health",
            filter={"timestamp": {"$gte": start_date, "$lt": end_date}},
            sorter=[("timestamp", -1)],
        )

        if not records:
            return f"# 爬虫健康趋势报告（最近 {days} 天）\n\n无健康记录\n"

        daily_stats = self._calculate_daily_stats(records)
        report = self._format_trend_report(days, daily_stats)
        return report

    def _calculate_daily_stats(self, records: List[dict]) -> Dict:
        """按天计算统计数据"""
        daily_stats = {}
        for record in records:
            date_key = record["timestamp"].strftime("%Y-%m-%d")
            crawler_name = record["crawler_name"]

            if date_key not in daily_stats:
                daily_stats[date_key] = {}
            if crawler_name not in daily_stats[date_key]:
                daily_stats[date_key][crawler_name] = {"success": 0, "failed": 0}

            if record["success"]:
                daily_stats[date_key][crawler_name]["success"] += 1
            else:
                daily_stats[date_key][crawler_name]["failed"] += 1

        return daily_stats

    def _format_trend_report(self, days: int, daily_stats: Dict) -> str:
        """格式化趋势报告"""
        report = f"# 爬虫健康趋势报告（最近 {days} 天）\n\n"
        report += f"**统计天数**: {len(daily_stats)} 天\n\n"

        # 按爬虫汇总
        crawler_summary = {}
        for date_key, crawlers in daily_stats.items():
            for crawler_name, stat in crawlers.items():
                if crawler_name not in crawler_summary:
                    crawler_summary[crawler_name] = {"success": 0, "failed": 0}
                crawler_summary[crawler_name]["success"] += stat["success"]
                crawler_summary[crawler_name]["failed"] += stat["failed"]

        report += "## 爬虫成功率汇总\n\n"
        report += "| 爬虫名称 | 成功次数 | 失败次数 | 成功率 |\n"
        report += "|---------|---------|---------|--------|\n"

        for crawler_name, stat in sorted(crawler_summary.items()):
            total = stat["success"] + stat["failed"]
            success_rate = (stat["success"] / total * 100) if total > 0 else 0
            report += f"| {crawler_name} | {stat['success']} | {stat['failed']} | {success_rate:.1f}% |\n"

        return report
