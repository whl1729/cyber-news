## ADDED Requirements

### Requirement: Crawl DHH Blog posts
The system SHALL crawl https://world.hey.com/dhh and extract blog post metadata.

#### Scenario: Crawl returns posts
- **WHEN** crawler runs against https://world.hey.com/dhh
- **THEN** posts are stored in MongoDB collection `dhh_blog` with fields: id (title), url, created_at (YYYY-MM-DD), crawled_at

#### Scenario: Reporter renders section
- **WHEN** reporter runs
- **THEN** a "DHH Blog" section appears with posts sorted by created_at descending
