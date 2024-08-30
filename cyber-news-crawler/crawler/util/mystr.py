import re


def extract_leading_numbers(s: str) -> int:
    match = re.match(r"(\d+)", s)
    if match:
        return int(match.group(1))
    return 0
