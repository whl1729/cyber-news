## ADDED Requirements

### Requirement: Crawl Addy Osmani Blog posts
The system SHALL crawl https://addyosmani.com/blog/ and extract blog post metadata.

#### Scenario: Crawl returns posts
- **WHEN** crawler runs against https://addyosmani.com/blog/
- **THEN** posts are stored in MongoDB collection `addy_osmani_blog` with fields: id (title), url, created_at (YYYY-MM-DD), crawled_at

#### Scenario: Reporter renders section
- **WHEN** reporter runs
- **THEN** an "Addy Osmani Blog" section appears with posts sorted by created_at descending
