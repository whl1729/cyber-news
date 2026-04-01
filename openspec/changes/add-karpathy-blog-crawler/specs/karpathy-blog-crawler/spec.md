## ADDED Requirements

### Requirement: Crawl Karpathy blog index page
The system SHALL fetch `https://karpathy.github.io` using `myrequests.get()` with proxy configuration and parse the HTML response to extract all blog posts.

#### Scenario: Successful fetch
- **WHEN** the crawler runs and the site is reachable
- **THEN** the HTML response is saved via `fs.save_response_text()` and parsed for blog posts

#### Scenario: Fetch failure
- **WHEN** the HTTP request returns no response after all retries
- **THEN** the crawler logs an error and returns `False`

### Requirement: Parse blog post list
The system SHALL parse `<ul class="posts">` from the index page and extract each `<li>` item's title, URL, date (YYYY-MM-DD), and description.

#### Scenario: Parse valid post list
- **WHEN** HTML contains `<ul class="posts">` with `<li>` items
- **THEN** each item's title (from `<a class="post-link">`), href, date (from `<span class="post-date">`), and description text SHALL be extracted

#### Scenario: Date parsing
- **WHEN** date text is in "Mon DD, YYYY" format (e.g., "Feb 12, 2026")
- **THEN** `created_at` SHALL be stored as "YYYY-MM-DD" (e.g., "2026-02-12")

#### Scenario: Invalid date format
- **WHEN** a post's date cannot be parsed
- **THEN** a warning SHALL be logged and that post SHALL be skipped

### Requirement: Store posts in MongoDB
The system SHALL store parsed posts in MongoDB collection `karpathy_blog` using `mongo.insert_many_new()` with `id` as the unique key (set to the post's relative href).

#### Scenario: New posts inserted
- **WHEN** posts are fetched that don't already exist in the collection
- **THEN** they SHALL be inserted and the count logged as "N karpathy blog posts inserted"

#### Scenario: Duplicate posts skipped
- **WHEN** posts already exist in the collection (same `id`)
- **THEN** they SHALL not be re-inserted (deduplication via `insert_many_new`)

### Requirement: Register crawler in ai_crawler
The system SHALL register `karpathy_blog_crawler` in `ai_crawler.py` under the topic key `"karpathy_blog"` using the existing `dict` + `get_enabled_topics()` pattern.

#### Scenario: Topic enabled
- **WHEN** `karpathy_blog` is in enabled topics (or enabled_topics is None)
- **THEN** `karpathy_blog_crawler.crawl()` SHALL be called

#### Scenario: Topic disabled
- **WHEN** `karpathy_blog` is not in enabled topics
- **THEN** the crawler SHALL be skipped with an info log

### Requirement: Display in daily news report
The system SHALL display Karpathy blog posts in the daily news report under the section "Karpathy Blog", ordered by `created_at` descending.

#### Scenario: Posts displayed in report
- **WHEN** the reporter runs and `karpathy_blog` collection has posts
- **THEN** a "Karpathy Blog" section SHALL appear in the generated Markdown with posts sorted newest-first
