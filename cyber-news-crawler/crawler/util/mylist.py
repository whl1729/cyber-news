def first(arr: list, default=""):
    return arr[0] if arr else default


def strip_join(arr: list):
    """strip whitespaces of any elements in a list and join them"""
    return "".join(arr).replace("\n", " ").replace("  ", "").strip()
