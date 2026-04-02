## ADDED Requirements

### Requirement: Crawl Mario Zechner Blog posts
The system SHALL crawl https://mariozechner.at and extract blog post metadata.

#### Scenario: Crawl returns posts
- **WHEN** crawler runs against https://mariozechner.at
- **THEN** posts are stored in MongoDB collection `mario_zechner_blog` with fields: id (title), url, created_at (YYYY-MM-DD), crawled_at

#### Scenario: Reporter renders section
- **WHEN** reporter runs
- **THEN** a "Mario Zechner Blog" section appears with posts sorted by created_at descending
