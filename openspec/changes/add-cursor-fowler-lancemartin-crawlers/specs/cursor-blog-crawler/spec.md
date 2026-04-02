## ADDED Requirements

### Requirement: Crawl Cursor blog posts
The crawler SHALL fetch `https://cursor.com/blog`, parse all blog article links, and store them in the `cursor_blog` MongoDB collection. Each article SHALL be stored with fields: `id` (article title), `url` (full absolute URL), `created_at` (ISO date YYYY-MM-DD), `crawled_at` (timestamp).

#### Scenario: Successful crawl
- **WHEN** the crawler fetches https://cursor.com/blog
- **THEN** it SHALL return one or more blog post entries with non-empty `id`, `url`, and `created_at` fields

#### Scenario: Duplicate articles skipped
- **WHEN** the same article has already been stored in `cursor_blog`
- **THEN** `insert_many_new()` SHALL skip duplicates without error

#### Scenario: Invalid or missing date
- **WHEN** a blog post entry has no parseable date
- **THEN** the item SHALL be skipped and a warning SHALL be logged

### Requirement: Register Cursor blog crawler
The `cursor_blog` topic SHALL be registered in `ai_crawler.py` under the key `"cursor_blog"` and SHALL be enabled in `config/cyber_news_config.yaml`.

#### Scenario: Topic enabled
- **WHEN** `enabled_topics` includes `"cursor_blog"`
- **THEN** the crawler SHALL run as part of `ai_crawler.crawl()`

### Requirement: Report Cursor blog in daily news
A `DailyNewsReporter` instance with `title="Cursor Blog"`, `table_name="cursor_blog"`, and `order_by="created_at"` SHALL be included in `news_reporter.py`'s `report_daily_news()`.

#### Scenario: Report generated
- **WHEN** `news_reporter.report()` is called and `cursor_blog` collection has documents
- **THEN** the output Markdown SHALL contain a `## Cursor Blog` section
