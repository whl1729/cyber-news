## ADDED Requirements

### Requirement: Crawl antirez Blog posts
The system SHALL crawl https://antirez.com/latest/0 and extract blog post metadata.

#### Scenario: Crawl returns posts
- **WHEN** crawler runs against https://antirez.com/latest/0
- **THEN** posts are stored in MongoDB collection `antirez_blog` with fields: id (title), url, created_at (YYYY-MM-DD), crawled_at

#### Scenario: Reporter renders section
- **WHEN** reporter runs
- **THEN** an "antirez Blog" section appears with posts sorted by created_at descending
