## ADDED Requirements

### Requirement: Crawl Han Not Solo Blog posts
The system SHALL crawl https://leehanchung.github.io/blogs/ and extract blog post metadata.

#### Scenario: Crawl returns posts
- **WHEN** crawler runs against https://leehanchung.github.io/blogs/
- **THEN** posts are stored in MongoDB collection `han_not_solo_blog` with fields: id (title), url, created_at (YYYY-MM-DD), crawled_at

#### Scenario: Reporter renders section
- **WHEN** reporter runs
- **THEN** a "Han, Not Solo Blog" section appears with posts sorted by created_at descending
