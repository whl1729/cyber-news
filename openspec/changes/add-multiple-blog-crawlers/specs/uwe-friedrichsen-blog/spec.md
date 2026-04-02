## ADDED Requirements

### Requirement: Crawl Uwe Friedrichsen Blog posts
The system SHALL crawl https://www.ufried.com/ and extract blog post metadata.

#### Scenario: Crawl returns posts
- **WHEN** crawler runs against https://www.ufried.com/
- **THEN** posts are stored in MongoDB collection `uwe_friedrichsen_blog` with fields: id (title), url, created_at (YYYY-MM-DD), crawled_at

#### Scenario: Reporter renders section
- **WHEN** reporter runs
- **THEN** a "Uwe Friedrichsen Blog" section appears with posts sorted by created_at descending
