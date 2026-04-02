## ADDED Requirements

### Requirement: Crawl Chris Gregori Blog posts
The system SHALL crawl https://www.chrisgregori.dev/ and extract blog post metadata.

#### Scenario: Crawl returns posts
- **WHEN** crawler runs against https://www.chrisgregori.dev/
- **THEN** posts are stored in MongoDB collection `chris_gregori_blog` with fields: id (title), url, created_at (YYYY-MM-DD), crawled_at

#### Scenario: Reporter renders section
- **WHEN** reporter runs
- **THEN** a "Chris Gregori Blog" section appears with posts sorted by created_at descending
