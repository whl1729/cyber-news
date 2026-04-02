## ADDED Requirements

### Requirement: Crawl Sean Goedecke Blog posts
The system SHALL crawl https://www.seangoedecke.com and extract blog post metadata.

#### Scenario: Crawl returns posts
- **WHEN** crawler runs against https://www.seangoedecke.com
- **THEN** posts are stored in MongoDB collection `sean_goedecke_blog` with fields: id (title), url, created_at (YYYY-MM-DD), crawled_at

#### Scenario: Reporter renders section
- **WHEN** reporter runs
- **THEN** a "Sean Goedecke Blog" section appears with posts sorted by created_at descending
