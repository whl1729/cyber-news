## ADDED Requirements

### Requirement: Crawl BaoYu Blog posts
The system SHALL crawl https://baoyu.io/ and extract blog post metadata.

#### Scenario: Crawl returns posts
- **WHEN** crawler runs against https://baoyu.io/
- **THEN** posts are stored in MongoDB collection `baoyu_blog` with fields: id (title), url, created_at (YYYY-MM-DD), crawled_at

#### Scenario: Reporter renders section
- **WHEN** reporter runs
- **THEN** a "BaoYu Blog" section appears with posts sorted by created_at descending
