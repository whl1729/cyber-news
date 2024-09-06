"""
This module gets time information.
"""
from datetime import datetime
from datetime import timedelta

import pytz

from news.util import mystr
from news.util.logger import logger


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
    now = datetime.now()
    return f"{now.year}年{now.month}月{now.day}日"


def yesterday():
    yesterday = datetime.now() - timedelta(1)
    return yesterday.strftime("%Y-%m-%d")


def yesterday2():
    yesterday = datetime.now() - timedelta(1)
    return yesterday.strftime("%Y年%m月%d日")


def n_days_ago(n: int):
    days_ago = datetime.now() - timedelta(n)
    return days_ago.strftime("%Y-%m-%d")


def n_hours_ago(n: int):
    hours_ago = datetime.now() - timedelta(hours=n)
    return hours_ago.strftime("%Y-%m-%d %H:%M:%S")


def n_minutes_ago(n: int):
    minutes_ago = datetime.now() - timedelta(minutes=n)
    return minutes_ago.strftime("%Y-%m-%d %H:%M:%S")


def format_date(date_str: str) -> str:
    """
    :param date_str: 日期字符串，示例："2 May 2024"
    """
    try:
        date_obj = datetime.strptime(date_str, "%d %B %Y")
        return date_obj.strftime("%Y-%m-%d")
    except ValueError as e:
        logger.warn(f"Failed to format date: {e}")
        return date_str


def format_date_2(date_str: str):
    """
    :param date_str: 时间字符串，示例："May 2 2024"
    """
    try:
        date_str = date_str.replace("July", "Jul")
        date_str = date_str.replace("June", "Jun")
        date_obj = datetime.strptime(date_str, "%b %d %Y")
        return date_obj.strftime("%Y-%m-%d")
    except ValueError as e:
        logger.warn(f"2.1 Failed to format date: {e}")
        try:
            date_obj = datetime.strptime(date_str, "%B %d %Y")
            return date_obj.strftime("%Y-%m-%d")
        except ValueError as e:
            logger.warn(f"2.2 Failed to format date again: {e}")
            return date_str


def format_date_3(date_str: str) -> str:
    """
    :param date_str: 日期字符串，示例："September 3, 2024"
    """
    try:
        date_obj = datetime.strptime(date_str, "%B %d, %Y")
        return date_obj.strftime("%Y-%m-%d")
    except ValueError as e:
        logger.warn(f"Failed to format date: {e}")
        return date_str


def format_time(time_str: str) -> str:
    """
    :param time_str: 时间字符串，示例："Sep 2, 2024 02:13 PM"
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
    except ValueError as e:
        logger.warn(f"Failed to format time: {e}")
        return time_str


def format_time_2(time_str: str) -> str:
    """
    :param time_str: 时间字符串，示例："Tue, 11 Jul 2023 20:08:00 +0000"
    """
    try:
        # 解析日期时间字符串为 datetime 对象
        date_obj = datetime.strptime(time_str, "%a, %d %b %Y %H:%M:%S %z")

        # 将 datetime 对象格式化为所需的字符串格式
        return date_obj.strftime("%Y-%m-%d %H:%M:%S")
    except ValueError as e:
        logger.warn(f"2. Failed to format time: {e}")
        return time_str


def format_iso_time(iso_time_str: str):
    try:
        dt = datetime.strptime(iso_time_str, "%Y-%m-%dT%H:%M:%SZ")
        dt = dt.replace(tzinfo=pytz.UTC)
        tz = pytz.timezone("Asia/Shanghai")
        dt = dt.astimezone(tz)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except ValueError as e:
        logger.warn(f"Failed to format iso time: {e}")
        return iso_time_str


def format_iso8601_time(iso8601_str: str):
    """
    :param iso8601_str: ISO 8601 日期字符串，例如："2024-08-30T08:08:59+08:00"
    """
    try:
        # 解析带有时区信息的 ISO 8601 日期字符串
        dt_with_timezone = datetime.fromisoformat(iso8601_str)
        # 将日期时间转换为不带时区信息的字符串
        dt_without_timezone = dt_with_timezone.strftime("%Y-%m-%d %H:%M:%S")
        return dt_without_timezone
    except ValueError as e:
        logger.warn(f"Failed to format iso8601 time: {e}")
        return iso8601_str


def format_iso8601_time_2(iso8601_str: str):
    """
    :param iso8601_str: ISO 8601 日期字符串，例如："2024-09-04T21:37:33.000000Z" 或 "2024-09-04T21:37:33"
    """
    try:
        # 解析日期时间字符串为 datetime 对象
        if iso8601_str.endswith("Z"):
            parsed_date = datetime.strptime(iso8601_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        else:
            parsed_date = datetime.strptime(iso8601_str, "%Y-%m-%dT%H:%M:%S")
        # 将 datetime 对象格式化为所需的字符串格式
        return parsed_date.strftime("%Y-%m-%d %H:%M:%S")
    except ValueError as e:
        logger.warn(f"Failed to format iso8601 time: {e}")
        return iso8601_str


def parse_time(time_str: str) -> str:
    if "分钟前" in time_str:
        minutes = mystr.extract_leading_numbers(time_str)
        return n_minutes_ago(minutes)

    if "小时前" in time_str:
        hours = mystr.extract_leading_numbers(time_str)
        return n_hours_ago(hours)

    if "天前" in time_str:
        days = mystr.extract_leading_numbers(time_str)
        return n_days_ago(days)

    if "昨天" in time_str:
        return time_str.replace("昨天", yesterday())

    if "前天" in time_str:
        return time_str.replace("前天", n_days_ago(2))

    try:
        date_obj = datetime.strptime(time_str, "%Y/%m/%d")
        return date_obj.strftime("%Y-%m-%d")
    except ValueError as _:
        pass

    return time_str
