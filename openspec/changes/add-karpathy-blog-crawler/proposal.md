## Why

Andrej Karpathy's blog contains high-quality AI research insights and is a valuable source for AI practitioners. Adding it to the daily news feed keeps users informed of new posts from one of the most influential AI researchers.

## What Changes

- Add `karpathy_blog_crawler.py` in `news/crawler/ai/` to fetch and parse posts from `https://karpathy.github.io`
- Register the new crawler in `news/crawler/ai/ai_crawler.py` using the existing `dict` + `get_enabled_topics()` pattern
- Add a `DailyNewsReporter` entry for Karpathy blog in `news/reporter/news_reporter.py` with `order_by="created_at"`

## Capabilities

### New Capabilities

- `karpathy-blog-crawler`: Crawls `https://karpathy.github.io`, parses post list (`<ul class="posts">`), extracts title, URL, date, and description; stores in MongoDB collection `karpathy_blog`

### Modified Capabilities

## Impact

- New file: `news/crawler/ai/karpathy_blog_crawler.py`
- Modified: `news/crawler/ai/ai_crawler.py` (add crawler registration)
- Modified: `news/reporter/news_reporter.py` (add DailyNewsReporter)
- No new dependencies required (uses existing `requests`, `BeautifulSoup`)
