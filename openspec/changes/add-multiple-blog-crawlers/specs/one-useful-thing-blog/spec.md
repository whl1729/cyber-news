## ADDED Requirements

### Requirement: Crawl One Useful Thing Blog posts
The system SHALL crawl https://www.oneusefulthing.org and extract blog post metadata.

#### Scenario: Crawl returns posts
- **WHEN** crawler runs against https://www.oneusefulthing.org
- **THEN** posts are stored in MongoDB collection `one_useful_thing_blog` with fields: id (title), url, created_at (YYYY-MM-DD), crawled_at

#### Scenario: Reporter renders section
- **WHEN** reporter runs
- **THEN** a "One Useful Thing" section appears with posts sorted by created_at descending
