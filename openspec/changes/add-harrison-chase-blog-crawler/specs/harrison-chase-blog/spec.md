## ADDED Requirements

### Requirement: Crawl blog posts from Harrison Chase's Weblog
The system SHALL crawl blog posts from blog.langchain.com/author/harrison/ and extract title, URL, and publication date for each post.

#### Scenario: Successful crawl of blog page
- **WHEN** crawler fetches blog.langchain.com/author/harrison/
- **THEN** it shall parse all blog post entries
- **AND** extract the title from the post card h2 anchor text
- **AND** extract the URL from the post card h2 or media href attribute
- **AND** prepend https://blog.langchain.com to form the full URL if needed
- **AND** extract the publication date from the image filename if available
- **AND** parse the date from format like `Screenshot-YYYY-MM-DD-at-HH.MM.SS---AM/PM.png` or `Screenshot-YYYY-MM-DD-at-HH.MM.SS---AM-1.png` to ISO 8601 format (YYYY-MM-DD)
- **AND** store each post in the harrison_chase_blog collection with id, url, created_at, and crawled_at fields

#### Scenario: Parse date from image filename
- **WHEN** publication date is available in image filename pattern like `Screenshot-2026-02-09-at-9.30.02---PM.png`
- **THEN** parse and extract the date components (year, month, day, hour, minute, second, AM/PM)
- **THEN** convert 12-hour format with AM/PM to 24-hour format
- **AND** convert to ISO 8601 format (YYYY-MM-DD)
- **AND** store in the created_at field

#### Scenario: Fallback date when image filename unavailable
- **WHEN** publication date cannot be extracted from image filename
- **THEN** use crawled_at timestamp as the created_at value for ordering
- **AND** store in the created_at field

### Requirement: Store blog posts in MongoDB
The system SHALL store crawled blog posts in the harrison_chase_blog collection, avoiding duplicate entries based on the id field.

#### Scenario: Insert new blog posts
- **WHEN** crawling completes with N new blog posts
- **THEN** insert N documents into harrison_chase_blog collection
- **AND** log "N harrison chase blog inserted" with the count

#### Scenario: Skip duplicate blog posts
- **WHEN** a blog post with the same id already exists in the collection
- **THEN** skip insertion of the duplicate post
- **AND** log only the count of newly inserted posts

### Requirement: Generate daily news report for Harrison Chase blog
The system SHALL generate a daily news report section for Harrison Chase Blog, listing blog posts ordered by publication date from newest to oldest.

#### Scenario: Generate daily news report section
- **WHEN** the daily news reporter runs
- **THEN** create a section titled "## Harrison Chase Blog"
- **AND** query the harrison_chase_blog collection for posts from the last 7 days
- **AND** order results by created_at in descending order
- **AND** format each post as a Markdown link with the publication date
- **AND** log "Harrison Chase Blog count: N" with the count

#### Scenario: Format blog post entry in report
- **WHEN** formatting a blog post for the report
- **THEN** display as "- [YYYY-MM-DD](url) title"
- **WHERE** YYYY-MM-DD is the publication date, url is the full post URL, and title is the post title

### Requirement: Enable/disable crawler via configuration
The system SHALL allow enabling or disabling the Harrison Chase blog crawler through the enabled_topics configuration in cyber_news_config.yaml.

#### Scenario: Enable crawler via configuration
- **WHEN** enabled_topics contains "harrison_chase_blog"
- **THEN** execute the Harrison Chase blog crawler during the crawl phase

#### Scenario: Disable crawler via configuration
- **WHEN** enabled_topics is set but does not contain "harrison_chase_blog"
- **THEN** skip the Harrison Chase blog crawler
- **AND** log "Skipping harrison_chase_blog (not in enabled_topics)"
