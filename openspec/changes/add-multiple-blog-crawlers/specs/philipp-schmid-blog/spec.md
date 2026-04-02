## ADDED Requirements

### Requirement: Crawl Philipp Schmid Blog posts
The system SHALL crawl https://www.philschmid.de and extract blog post metadata.

#### Scenario: Crawl returns posts
- **WHEN** crawler runs against https://www.philschmid.de
- **THEN** posts are stored in MongoDB collection `philipp_schmid_blog` with fields: id (title), url, created_at (YYYY-MM-DD), crawled_at

#### Scenario: Reporter renders section
- **WHEN** reporter runs
- **THEN** a "Philipp Schmid Blog" section appears with posts sorted by created_at descending
