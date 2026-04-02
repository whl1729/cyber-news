## ADDED Requirements

### Requirement: Crawl Bassim Eledath Blog posts
The system SHALL crawl https://www.bassimeledath.com/blog and extract blog post metadata.

#### Scenario: Crawl returns posts
- **WHEN** crawler runs against https://www.bassimeledath.com/blog
- **THEN** posts are stored in MongoDB collection `bassim_eledath_blog` with fields: id (title), url, created_at (YYYY-MM-DD), crawled_at

#### Scenario: Reporter renders section
- **WHEN** reporter runs
- **THEN** a "Bassim Eledath Blog" section appears with posts sorted by created_at descending
