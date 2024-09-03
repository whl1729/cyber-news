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
