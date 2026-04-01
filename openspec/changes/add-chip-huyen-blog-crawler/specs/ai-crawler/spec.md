## ADDED Requirements

### Requirement: Register chip_huyen_blog in AI crawler
The `ai_crawler.py` dispatcher SHALL include `"chip_huyen_blog": chip_huyen_blog_crawler` in its crawlers dict so it participates in the enabled-topics gating mechanism.

#### Scenario: chip_huyen_blog crawler runs via ai_crawler
- **WHEN** `ai_crawler.crawl()` is called and `chip_huyen_blog` is in enabled topics
- **THEN** `chip_huyen_blog_crawler.crawl()` SHALL be invoked
