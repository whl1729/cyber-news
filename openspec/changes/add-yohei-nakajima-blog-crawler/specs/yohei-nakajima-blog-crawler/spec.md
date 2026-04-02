## ADDED Requirements

### Requirement: Crawl blog posts from Yohei Nakajima's website
The system SHALL fetch blog posts from https://yoheinakajima.com/blog/ and extract structured data including title, URL, and publication date.

#### Scenario: Successfully fetch blog posts
- **WHEN** the crawler runs
- **THEN** it SHALL retrieve the blog listing page
- **THEN** it SHALL parse all blog post entries from the page

#### Scenario: Extract blog post metadata
- **WHEN** parsing a blog post entry
- **THEN** it SHALL extract the post title
- **THEN** it SHALL extract the post URL
- **THEN** it SHALL extract the publication date in YYYY-MM-DD format

### Requirement: Store blog posts in MongoDB
The system SHALL store crawled blog posts in a MongoDB collection named `yohei_nakajima_blog`.

#### Scenario: Insert new blog posts
- **WHEN** new blog posts are crawled
- **THEN** they SHALL be inserted into the `yohei_nakajima_blog` collection
- **THEN** duplicate posts SHALL be skipped based on URL

#### Scenario: Store required fields
- **WHEN** storing a blog post
- **THEN** it SHALL include `title` field
- **THEN** it SHALL include `url` field
- **THEN** it SHALL include `created_at` field with publication date
- **THEN** it SHALL include `crawled_at` field with current timestamp

### Requirement: Follow existing crawler patterns
The crawler SHALL follow the same implementation patterns as other blog crawlers in the `news/crawler/ai/` directory.

#### Scenario: Use web crawler utility
- **WHEN** implementing the crawler
- **THEN** it SHALL use the `WebCrawler` class from `news.util.web_crawler`
- **THEN** it SHALL implement a `crawl()` function as the entry point

#### Scenario: Logging and error handling
- **WHEN** the crawler runs
- **THEN** it SHALL log the number of posts parsed
- **THEN** it SHALL log the number of posts inserted
- **THEN** it SHALL handle network errors gracefully
