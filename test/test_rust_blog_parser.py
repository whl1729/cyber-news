from news.crawler.language.rust.rust_blog_crawler import RustBlogParser
from news.util import fs


def test_rust_blog_parser():
    html_path = fs.log_dir / "rust_blog_0.html"
    with open(html_path, encoding="utf-8") as f:
        content = f.read()
    parser = RustBlogParser()
    blog_list = parser.parse(content)
    assert blog_list[0]["id"] == "2024 Leadership Council Survey"
    assert (
        blog_list[0]["url"]
        == "https://blog.rust-lang.org/2024/08/26/council-survey.html"
    )
    assert blog_list[0]["created_at"] == "2024-08-26"


if __name__ == "__main__":
    test_rust_blog_parser()
