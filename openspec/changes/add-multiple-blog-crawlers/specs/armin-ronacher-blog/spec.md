## ADDED Requirements

### Requirement: Crawl Armin Ronacher Blog posts
The system SHALL crawl https://lucumr.pocoo.org and extract blog post metadata.

#### Scenario: Crawl returns posts
- **WHEN** crawler runs against https://lucumr.pocoo.org
- **THEN** posts are stored in MongoDB collection `armin_ronacher_blog` with fields: id (title), url, created_at (YYYY-MM-DD), crawled_at

#### Scenario: Reporter renders section
- **WHEN** reporter runs
- **THEN** an "Armin Ronacher Blog" section appears with posts sorted by created_at descending
