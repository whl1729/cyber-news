## ADDED Requirements

### Requirement: Crawl blog posts from Sebastian Raschka's website
The system SHALL crawl blog posts from sebastianraschka.com and extract title, URL, publication date, and optional description for each post.

#### Scenario: Successful crawl of blog page
- **WHEN** the crawler fetches sebastianraschka.com
- **THEN** it shall parse all blog post entries
- **AND** extract the title from the post title anchor text
- **AND** extract the URL from the post title href attribute (handling both absolute and relative URLs)
- **AND** extract the publication date from the post-date element
- **AND** extract the description text from the post-description element if present
- **AND** store each post in the sebastian_raschka_blog collection with id, url, created_at, and crawled_at fields

#### Scenario: Handle absolute and relative URLs
- **WHEN** a blog post link is a relative URL starting with /
- **THEN** prepend https://sebastianraschka.com to form the full URL
- **WHEN** a blog post link is an absolute URL starting with https://
- **THEN** use the URL as-is

#### Scenario: Parse date in "Month Day, Year" format
- **WHEN** the publication date is in format like "Mar 22, 2026"
- **THEN** parse and convert to ISO 8601 format (YYYY-MM-DD)
- **AND** store in the created_at field

### Requirement: Store blog posts in MongoDB
The system SHALL store crawled blog posts in the sebastian_raschka_blog collection, avoiding duplicate entries based on the id field.

#### Scenario: Insert new blog posts
- **WHEN** crawling completes with N new blog posts
- **THEN** insert N documents into sebastian_raschka_blog collection
- **AND** log "N sebastian raschka blog inserted" with the count

#### Scenario: Skip duplicate blog posts
- **WHEN** a blog post with the same id already exists in the collection
- **THEN** skip insertion of the duplicate post
- **AND** log only the count of newly inserted posts

### Requirement: Generate daily news report for Sebastian Raschka blog
The system SHALL generate a daily news report section for Sebastian Raschka Blog, listing blog posts ordered by publication date from newest to oldest.

#### Scenario: Generate daily news report section
- **WHEN** the daily news reporter runs
- **THEN** create a section titled "## Sebastian Raschka Blog"
- **AND** query the sebastian_raschka_blog collection for posts from the last 7 days
- **AND** order results by created_at in descending order
- **AND** format each post as a Markdown link with the publication date
- **AND** log "Sebastian Raschka Blog count: N" with the count

#### Scenario: Format blog post entry in report
- **WHEN** formatting a blog post for the report
- **THEN** display as "- [YYYY-MM-DD](url) title"
- **WHERE** YYYY-MM-DD is the publication date, url is the full post URL, and title is the post title

### Requirement: Enable/disable crawler via configuration
The system SHALL allow enabling or disabling the Sebastian Raschka blog crawler through the enabled_topics configuration in cyber_news_config.yaml.

#### Scenario: Enable crawler via configuration
- **WHEN** enabled_topics contains "sebastian_raschka_blog"
- **THEN** execute the Sebastian Raschka blog crawler during the crawl phase

#### Scenario: Disable crawler via configuration
- **WHEN** enabled_topics is set but does not contain "sebastian_raschka_blog"
- **THEN** skip the Sebastian Raschka blog crawler
- **AND** log "Skipping sebastian_raschka_blog (not in enabled_topics)"
