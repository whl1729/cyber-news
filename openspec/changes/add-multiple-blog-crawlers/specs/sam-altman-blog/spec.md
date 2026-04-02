## ADDED Requirements

### Requirement: Crawl Sam Altman Blog posts
The system SHALL crawl https://blog.samaltman.com/ and extract blog post metadata.

#### Scenario: Crawl returns posts
- **WHEN** crawler runs against https://blog.samaltman.com/
- **THEN** posts are stored in MongoDB collection `sam_altman_blog` with fields: id (title), url, created_at (YYYY-MM-DD), crawled_at

#### Scenario: Reporter renders section
- **WHEN** reporter runs
- **THEN** a "Sam Altman Blog" section appears with posts sorted by created_at descending
