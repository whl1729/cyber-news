## 1. Cursor Blog Crawler

- [x] 1.1 Create `news/crawler/ai/cursor_blog_crawler.py` — implement `CursorBlogParser(WebParser)` that parses `<a href="/blog/...">` links from `cursor.com/blog` and extracts title, URL, and date from anchor text (format: `"Mar 19, 2026·Research..."`)
- [x] 1.2 Add `crawl()` function to `cursor_blog_crawler.py` using `web_crawler.crawl()` with `COLLECTION_NAME = "cursor_blog"` and `proxies=config["proxies"]`
- [x] 1.3 Register `cursor_blog` in `news/crawler/ai/ai_crawler.py` (import + dict entry)
- [x] 1.4 Add `DailyNewsReporter("Cursor Blog", "cursor_blog", order_by="created_at")` to `report_daily_news()` in `news/reporter/news_reporter.py`
- [x] 1.5 Add `cursor_blog` to `enabled_topics` in `config/cyber_news_config.yaml`
- [x] 1.6 Verify: run `./script/run.sh -p news/crawler/ai/cursor_blog_crawler.py -l debug` and confirm entries are inserted

## 2. Martin Fowler Exploring Gen AI Crawler

- [x] 2.1 Create `news/crawler/ai/martin_fowler_gen_ai_crawler.py` — implement `MartinFowlerGenAIParser(WebParser)` that finds `<p class="memo">` elements, extracts article `<a>` title + href, and parses `<span class="date">` text like `(04 March 2026)` → `"2026-03-04"`
- [x] 2.2 Add `crawl()` function using `web_crawler.crawl()` targeting `https://martinfowler.com/articles/exploring-gen-ai.html` with `COLLECTION_NAME = "martin_fowler_gen_ai"`
- [x] 2.3 Register `martin_fowler_gen_ai` in `news/crawler/ai/ai_crawler.py`
- [x] 2.4 Add `DailyNewsReporter("Martin Fowler: Exploring Gen AI", "martin_fowler_gen_ai", order_by="created_at")` to `report_daily_news()`
- [x] 2.5 Add `martin_fowler_gen_ai` to `enabled_topics` in `config/cyber_news_config.yaml`
- [x] 2.6 Verify: run crawler and confirm episodes are inserted

## 3. Lance Martin Blog Crawler

- [x] 3.1 Create `news/crawler/ai/lance_martin_blog_crawler.py` — implement `LanceMartinBlogParser(WebParser)` that finds `<li>` items in `<ul class="post-list">`, extracts title from `<a class="post-link">`, date from `<span class="post-meta">` (format: `"Jan 9, 2026"`), and resolves relative hrefs to full URLs
- [x] 3.2 Add `crawl()` function targeting `https://rlancemartin.github.io` with `COLLECTION_NAME = "lance_martin_blog"`
- [x] 3.3 Register `lance_martin_blog` in `news/crawler/ai/ai_crawler.py`
- [x] 3.4 Add `DailyNewsReporter("Lance Martin Blog", "lance_martin_blog", order_by="created_at")` to `report_daily_news()`
- [x] 3.5 Add `lance_martin_blog` to `enabled_topics` in `config/cyber_news_config.yaml`
- [x] 3.6 Verify: run crawler and confirm posts are inserted

## 4. Validation

- [x] 4.1 Run `./script/run.sh -p news/reporter/news_reporter.py -l debug` and confirm all three new sections appear in logs
- [x] 4.2 Check generated Markdown report for `## Cursor Blog`, `## Martin Fowler: Exploring Gen AI`, and `## Lance Martin Blog` sections with correct date ordering
- [x] 4.3 Run `pre-commit run --files` on all modified files and confirm all checks pass
