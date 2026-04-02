## ADDED Requirements

### Requirement: Crawl The Pragmatic Engineer Blog posts
The system SHALL crawl https://newsletter.pragmaticengineer.com and extract publicly available blog post metadata.

#### Scenario: Crawl returns posts
- **WHEN** crawler runs against https://newsletter.pragmaticengineer.com
- **THEN** posts are stored in MongoDB collection `pragmatic_engineer_blog` with fields: id (title), url, created_at (YYYY-MM-DD), crawled_at

#### Scenario: Reporter renders section
- **WHEN** reporter runs
- **THEN** a "The Pragmatic Engineer" section appears with posts sorted by created_at descending
