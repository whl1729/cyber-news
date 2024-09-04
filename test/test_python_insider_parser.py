from news.crawler.language.python.python_insider_crawler import PythonInsiderParser
from news.util import fs


def test_python_insider_parser():
    html_path = fs.log_dir / "python_insider_0.xml"
    with open(html_path, encoding="utf-8") as f:
        content = f.read()
    parser = PythonInsiderParser()
    blog_list = parser.parse(content)
    assert blog_list[0]["id"] == "Python 3.12.5 released"
    assert (
        blog_list[0]["url"]
        == "https://pythoninsider.blogspot.com/2024/08/python-3125-released.html"
    )
    assert blog_list[0]["created_at"] == "2024-08-07 13:17:00"


if __name__ == "__main__":
    test_python_insider_parser()
