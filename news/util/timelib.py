"""
This module gets time information.
"""
from datetime import datetime
from datetime import timedelta

import pytz


def now() -> str:
    return datetime.now().strftime("%Y%m%d%H%M%S")


def now2() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def now3() -> str:
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def now4():
    tz = pytz.timezone("Asia/Shanghai")
    return datetime.now(tz).isoformat()


def today() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def today2():
    return datetime.now().strftime("%Y年%m月%d日")


def yesterday():
    yesterday = datetime.now() - timedelta(1)
    return yesterday.strftime("%Y-%m-%d")


def yesterday2():
    yesterday = datetime.now() - timedelta(1)
    return yesterday.strftime("%Y年%m月%d日")


def n_days_ago(n: int):
    days_ago = datetime.now() - timedelta(n)
    return days_ago.strftime("%Y-%m-%d")


def format_date(date_str: str) -> str:
    """
    :param date_str: 日期字符串，示例："2 May 2024"
    """
    try:
        date_obj = datetime.strptime(date_str, "%d %B %Y")
        return date_obj.strftime("%Y-%m-%d")
    except Exception as _:
        return date_str


def format_date_2(date_str: str):
    """
    :param date_str: 时间字符串，示例："May 2 2024"
    """
    try:
        date_obj = datetime.strptime(date_str, "%b %d %Y")
        return date_obj.strftime("%Y-%m-%d")
    except Exception as _:
        try:
            date_obj = datetime.strptime(date_str, "%B %d %Y")
            return date_obj.strftime("%Y-%m-%d")
        except Exception as _:
            return date_str


def format_time(time_str: str) -> str:
    """
    :param date_str: 时间字符串，示例："Sep 2, 2024 02:13 PM"
    """
    try:
        # 定义输入日期格式
        input_format = "%b %d, %Y %I:%M %p"

        # 将输入字符串解析为 datetime 对象
        date_obj = datetime.strptime(time_str, input_format)

        # 定义输出日期格式
        output_format = "%Y-%m-%d %H:%M"

        # 将 datetime 对象格式化为所需格式的字符串
        return date_obj.strftime(output_format)
    except Exception as _:
        return time_str


def format_iso_time(iso_time_str: str):
    dt = datetime.strptime(iso_time_str, "%Y-%m-%dT%H:%M:%SZ")
    dt = dt.replace(tzinfo=pytz.UTC)
    tz = pytz.timezone("Asia/Shanghai")
    dt = dt.astimezone(tz)
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def format_iso8601_time(iso8601_str: str):
    """
    :param iso8601_str: ISO 8601 日期字符串，例如："2024-08-30T08:08:59+08:00"
    """
    # 解析带有时区信息的 ISO 8601 日期字符串
    dt_with_timezone = datetime.fromisoformat(iso8601_str)
    # 将日期时间转换为不带时区信息的字符串
    dt_without_timezone = dt_with_timezone.strftime("%Y-%m-%d %H:%M:%S")
    return dt_without_timezone
