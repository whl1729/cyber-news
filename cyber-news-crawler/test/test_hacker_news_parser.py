from crawler.hacker_news.hacker_news_crawler import HackerNewsParser
from crawler.util import fs


def test_hacker_news_parse():
    html_path = fs.log_dir / "hacker_news.html"
    with open(html_path, encoding="utf-8") as f:
        content = f.read()
    parser = HackerNewsParser()
    result = parser.parse(content)
    assert len(result) == 30


if __name__ == "__main__":
    test_hacker_news_parse()
