## ADDED Requirements

### Requirement: Crawl Matt Shumer Blog posts
The system SHALL crawl https://shumer.dev/blog and extract blog post metadata.

#### Scenario: Crawl returns posts
- **WHEN** crawler runs against https://shumer.dev/blog
- **THEN** posts are stored in MongoDB collection `matt_shumer_blog` with fields: id (title), url, created_at (YYYY-MM-DD), crawled_at

#### Scenario: Reporter renders section
- **WHEN** reporter runs
- **THEN** a "Matt Shumer Blog" section appears with posts sorted by created_at descending
