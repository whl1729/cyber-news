## ADDED Requirements

### Requirement: Crawl Lance Martin's blog
The crawler SHALL fetch `https://rlancemartin.github.io`, parse all post entries from `<ul class="post-list">`, and store them in the `lance_martin_blog` MongoDB collection. Each entry SHALL have: `id` (post title), `url` (full absolute URL), `created_at` (ISO date YYYY-MM-DD), `crawled_at` (timestamp).

#### Scenario: Successful crawl
- **WHEN** the crawler fetches https://rlancemartin.github.io
- **THEN** it SHALL return one or more blog post entries with non-empty `id`, `url`, and `created_at`

#### Scenario: Date parsing from span.post-meta
- **WHEN** a post's `<span class="post-meta">` contains text like `Jan 9, 2026`
- **THEN** `created_at` SHALL be `"2026-01-09"`

#### Scenario: Relative URLs resolved
- **WHEN** a post link has a relative href like `/2026/01/09/agent_design/`
- **THEN** the stored `url` SHALL be `"https://rlancemartin.github.io/2026/01/09/agent_design/"`

### Requirement: Register Lance Martin blog crawler
The `lance_martin_blog` topic SHALL be registered in `ai_crawler.py` and enabled in `config/cyber_news_config.yaml`.

#### Scenario: Topic enabled
- **WHEN** `enabled_topics` includes `"lance_martin_blog"`
- **THEN** the crawler SHALL run as part of `ai_crawler.crawl()`

### Requirement: Report Lance Martin blog in daily news
A `DailyNewsReporter` with `title="Lance Martin Blog"`, `table_name="lance_martin_blog"`, and `order_by="created_at"` SHALL be in `report_daily_news()`.

#### Scenario: Report generated
- **WHEN** `news_reporter.report()` is called and the collection has documents
- **THEN** the Markdown SHALL contain a `## Lance Martin Blog` section
