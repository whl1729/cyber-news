## ADDED Requirements

### Requirement: Crawl Martin Fowler's Exploring Gen AI series
The crawler SHALL fetch `https://martinfowler.com/articles/exploring-gen-ai.html`, parse all episode links from `<p class="memo">` elements, and store them in the `martin_fowler_gen_ai` MongoDB collection. Each entry SHALL have fields: `id` (article title), `url` (full absolute URL), `created_at` (ISO date YYYY-MM-DD), `crawled_at` (timestamp).

#### Scenario: Successful crawl
- **WHEN** the crawler fetches the series index page
- **THEN** it SHALL return multiple episode entries with non-empty `id`, `url`, and `created_at`

#### Scenario: Date parsing from span.date
- **WHEN** an episode's `<span class="date">` contains text like `(04 March 2026)`
- **THEN** `created_at` SHALL be `"2026-03-04"`

#### Scenario: Missing date element
- **WHEN** a `<p class="memo">` entry has no `<span class="date">`
- **THEN** the item SHALL be skipped and a warning SHALL be logged

### Requirement: Register Martin Fowler Gen AI crawler
The `martin_fowler_gen_ai` topic SHALL be registered in `ai_crawler.py` and enabled in `config/cyber_news_config.yaml`.

#### Scenario: Topic enabled
- **WHEN** `enabled_topics` includes `"martin_fowler_gen_ai"`
- **THEN** the crawler SHALL run as part of `ai_crawler.crawl()`

### Requirement: Report Martin Fowler Gen AI in daily news
A `DailyNewsReporter` with `title="Martin Fowler: Exploring Gen AI"`, `table_name="martin_fowler_gen_ai"`, and `order_by="created_at"` SHALL be in `report_daily_news()`.

#### Scenario: Report generated
- **WHEN** `news_reporter.report()` is called and the collection has documents
- **THEN** the Markdown SHALL contain a `## Martin Fowler: Exploring Gen AI` section
