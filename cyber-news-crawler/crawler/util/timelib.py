"""
This module gets time information.
"""
from datetime import datetime


def now() -> str:
    return datetime.now().strftime("%Y%m%d%H%M%S")


def now2() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def now3() -> str:
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def today() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def format_date(date_str: str) -> str:
    """
    :param date_str: 日期字符串，示例："2 May 2024"
    """
    try:
        date_obj = datetime.strptime(date_str, "%d %B %Y")
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
