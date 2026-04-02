## 1. Inspect Blog Structure

- [x] 1.1 Visit https://deepmind.google/blog/ and inspect HTML structure
- [x] 1.2 Identify CSS selectors for blog post list, titles, URLs, and dates
- [x] 1.3 Verify date format and determine parsing strategy

## 2. Implement Crawler

- [x] 2.1 Create `news/crawler/ai/deepmind_blog_crawler.py`
- [x] 2.2 Implement `crawl()` function using WebCrawler pattern
- [x] 2.3 Parse blog post list from HTML using BeautifulSoup
- [x] 2.4 Extract title, URL, and publication date for each post
- [x] 2.5 Store posts in MongoDB collection `deepmind_blog` with fields: title, url, created_at, crawled_at
- [x] 2.6 Add logging for parsed count and inserted count

## 3. Register Crawler

- [x] 3.1 Import `deepmind_blog_crawler` in `news/crawler/ai/ai_crawler.py`
- [x] 3.2 Add `"deepmind_blog": deepmind_blog_crawler` to crawlers dict
- [x] 3.3 Verify crawler follows `get_enabled_topics()` pattern

## 4. Implement Reporter

- [x] 4.1 Create `news/reporter/deepmind_blog_reporter.py`
- [x] 4.2 Inherit from `DailyNewsReporter` base class
- [x] 4.3 Set collection name to `deepmind_blog`
- [x] 4.4 Set `order_by="created_at"` for chronological sorting
- [x] 4.5 Set section title to "DeepMind Blog"
- [x] 4.6 Format output as `- [title](url) (YYYY-MM-DD)`

## 5. Register Reporter

- [x] 5.1 Import `deepmind_blog_reporter` in `news/reporter/news_reporter.py`
- [x] 5.2 Add reporter call in the `report()` function

## 6. Configuration

- [x] 6.1 Add `deepmind_blog` to `enabled_topics` list in `config/cyber_news_config.yaml`

## 7. Testing

- [x] 7.1 Run crawler: `./script/run.sh -t deepmind_blog -l debug`
- [x] 7.2 Verify blog posts are crawled and inserted into MongoDB
- [x] 7.3 Run reporter: `./script/run.sh -p news/reporter/news_reporter.py -l debug`
- [x] 7.4 Verify "DeepMind Blog" section appears in report with posts sorted by date (newest first)
- [x] 7.5 Check logs show correct counts for parsed and inserted posts
