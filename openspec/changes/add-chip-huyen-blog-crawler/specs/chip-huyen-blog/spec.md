## ADDED Requirements

### Requirement: Crawl Chip Huyen blog posts
The crawler SHALL fetch `https://huyenchip.com/blog/`, parse the `<ul class="post-list">` element, and store each post as a document in the `chip_huyen_blog` MongoDB collection with fields: `id` (title string), `url` (absolute URL), `created_at` (YYYY-MM-DD date string), `crawled_at` (ISO datetime string).

#### Scenario: Successful crawl with posts
- **WHEN** the blog listing page is fetched and contains a `<ul class="post-list">` with post items
- **THEN** each `<li>` with a `<span class="post-meta">` date and `<a class="post-link">` link SHALL be parsed and inserted into the `chip_huyen_blog` collection

#### Scenario: Missing post list element
- **WHEN** the fetched HTML does not contain a `<ul class="post-list">` element
- **THEN** the crawler SHALL log a warning and return an empty list without raising an exception

#### Scenario: Individual item parse failure
- **WHEN** a `<li>` element is missing the date span or link element
- **THEN** that item SHALL be skipped with a warning log, and remaining items SHALL still be processed

### Requirement: Enable/disable via topic config
The `chip_huyen_blog` crawler SHALL be registered under topic key `"chip_huyen_blog"` in `ai_crawler.py` and MUST respect the `enabled_topics` configuration — skipping crawl if the topic is not listed.

#### Scenario: Topic enabled
- **WHEN** `chip_huyen_blog` is listed in `enabled_topics` (or `enabled_topics` is null)
- **THEN** the crawler SHALL run and attempt to fetch posts

#### Scenario: Topic disabled
- **WHEN** `chip_huyen_blog` is not listed in `enabled_topics`
- **THEN** the crawler SHALL be skipped and a skip log message SHALL be emitted
