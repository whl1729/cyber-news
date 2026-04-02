## ADDED Requirements

### Requirement: Crawl Ryan Dahl Blog posts
The system SHALL crawl https://tinyclouds.org and extract blog post metadata.

#### Scenario: Crawl returns posts
- **WHEN** crawler runs against https://tinyclouds.org
- **THEN** posts are stored in MongoDB collection `ryan_dahl_blog` with fields: id (title), url, created_at (YYYY-MM-DD), crawled_at

#### Scenario: Reporter renders section
- **WHEN** reporter runs
- **THEN** a "Ryan Dahl Blog" section appears with posts sorted by created_at descending
