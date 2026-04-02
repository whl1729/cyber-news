## ADDED Requirements

### Requirement: Crawl Rob Zolkos Blog posts
The system SHALL crawl https://www.zolkos.com/ and extract blog post metadata.

#### Scenario: Crawl returns posts
- **WHEN** crawler runs against https://www.zolkos.com/
- **THEN** posts are stored in MongoDB collection `rob_zolkos_blog` with fields: id (title), url, created_at (YYYY-MM-DD), crawled_at

#### Scenario: Reporter renders section
- **WHEN** reporter runs
- **THEN** a "Rob Zolkos Blog" section appears with posts sorted by created_at descending
