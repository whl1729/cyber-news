## 1. Inspect Blog Structure

- [x] 1.1 Use Selenium to fetch https://huggingface.co/blog with full rendering
- [x] 1.2 Identify HTML structure for blog post list (CSS selectors for containers, titles, URLs, dates)
- [x] 1.3 Determine date format and parsing strategy

## 2. Implement Crawler

- [x] 2.1 Create `news/crawler/ai/huggingface_blog_crawler.py`
- [x] 2.2 Implement `HuggingfaceBlogParser` class inheriting from `WebParser`
- [x] 2.3 Parse blog post list from HTML using BeautifulSoup
- [x] 2.4 Extract title, URL, and publication date for each post
- [x] 2.5 Implement date parsing with fallback to current date
- [x] 2.6 Implement `crawl()` function using `web_crawler.crawl()` with `use_selenium=True`
- [x] 2.7 Store posts in MongoDB collection `huggingface_blog` with fields: id (title), url, created_at, crawled_at
- [x] 2.8 Add logging for parsed count and inserted count

## 3. Register Crawler

- [x] 3.1 Import `huggingface_blog_crawler` in `news/crawler/ai/ai_crawler.py`
- [x] 3.2 Add `"huggingface_blog": huggingface_blog_crawler` to crawlers dict
- [x] 3.3 Verify crawler follows `get_enabled_topics()` pattern

## 4. Implement Reporter

- [x] 4.1 Create `news/reporter/huggingface_blog_reporter.py`
- [x] 4.2 Inherit from `DailyNewsReporter` base class
- [x] 4.3 Set collection name to `huggingface_blog`
- [x] 4.4 Set `order_by="created_at"` for chronological sorting
- [x] 4.5 Set section title to "Hugging Face Blog"
- [x] 4.6 Format output as `N. [title](url) (YYYY-MM-DD)`

## 5. Register Reporter

- [x] 5.1 Add reporter to `daily_reporters` list in `news/reporter/news_reporter.py`
- [x] 5.2 Verify reporter is called in `report_daily_news()` function

## 6. Configuration

- [x] 6.1 Add `huggingface_blog` to `enabled_topics` list in `config/cyber_news_config.yaml`

## 7. Testing

- [x] 7.1 Run crawler: `./script/run.sh -t huggingface_blog -l debug`
- [x] 7.2 Verify blog posts are crawled and inserted into MongoDB
- [x] 7.3 Run reporter: `./script/run.sh -p news/reporter/news_reporter.py -l debug`
- [x] 7.4 Verify "Hugging Face Blog" section appears in report with posts sorted by date (newest first)
- [x] 7.5 Check logs show correct counts for parsed and inserted posts
- [x] 7.6 Run pre-commit checks on all modified files
