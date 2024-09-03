"""
This module gets time information.
"""
from datetime import datetime


def now():
    return datetime.now().strftime("%Y%m%d%H%M%S")


def now2():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def now3():
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def today():
    return datetime.now().strftime("%Y-%m-%d")


def format_date(date_str: str):
    """
    :param date_str: 时间字符串，示例："2 May 2024"
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
