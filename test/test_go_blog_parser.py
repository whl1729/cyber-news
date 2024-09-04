from news.crawler.language.go.go_blog_crawler import GoBlogParser
from news.util import fs


def test_go_blog_parser():
    html_path = fs.log_dir / "go_blog_0.html"
    with open(html_path, encoding="utf-8") as f:
        content = f.read()
    parser = GoBlogParser()
    blog_list = parser.parse(content)
    assert blog_list[0]["id"] == "New unique package"
    assert blog_list[0]["url"] == "https://go.dev/blog/unique"
    assert blog_list[0]["author"] == "Michael Knyszek"
    assert blog_list[0]["summary"] == "New package for interning in Go 1.23."
    assert blog_list[0]["created_at"] == "2024-08-27"


if __name__ == "__main__":
    test_go_blog_parser()
