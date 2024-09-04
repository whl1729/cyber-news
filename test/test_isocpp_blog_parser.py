from news.crawler.language.cpp.isocpp_blog_crawler import IsocppBlogParser
from news.util import fs


def test_isocpp_blog_parser():
    html_path = fs.log_dir / "isocpp_blog_0.html"
    with open(html_path, encoding="utf-8") as f:
        content = f.read()
    parser = IsocppBlogParser()
    blog_list = parser.parse(content)
    assert (
        blog_list[0]["id"]
        == "CppCon 2024 When Nanoseconds Matter: Ultrafast Trading Systems in C++"
    )
    assert (
        blog_list[0]["url"]
        == "https://isocpp.org/blog/2024/09/cppcon-2024-when-nanoseconds-matter-ultrafast-trading-systems-in-cpp-david"
    )
    assert blog_list[0]["author"] == "David Gross"
    assert blog_list[0]["created_at"] == "2024-09-02 14:13"


if __name__ == "__main__":
    test_isocpp_blog_parser()
