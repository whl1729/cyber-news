## ADDED Requirements

### Requirement: Crawl blog posts from Simon Willison's Weblog
The system SHALL crawl blog posts from simonwillison.net/entries/ and extract title, URL, and publication date for each post.

#### Scenario: Successful crawl of blog page
- **WHEN** the crawler fetches simonwillison.net/entries/
- **THEN** it shall parse all blog post entries
- **AND** extract the title from the entry h3 anchor text
- **AND** extract the URL from the entry h3 href attribute
- **AND** prepend https://simonwillison.net to form the full URL
- **AND** extract the publication date from the entryFooter element
- **AND** parse the date from format like "30th March 2026" to ISO 8601 format (YYYY-MM-DD)
- **AND** store each post in the simon_willison_blog collection with id, url, created_at, and crawled_at fields

#### Scenario: Parse date with ordinal suffixes
- **WHEN** the publication date is in format like "30th March 2026", "27th March 2026", or "21st March 2026"
- **THEN** parse and remove the ordinal suffix (st, nd, rd, th)
- **AND** parse the month abbreviation (Mar) to number
- **AND** convert to ISO 8601 format (YYYY-MM-DD)
- **AND** store in the created_at field

### Requirement: Store blog posts in MongoDB
The system SHALL store crawled blog posts in the simon_willison_blog collection, avoiding duplicate entries based on the id field.

#### Scenario: Insert new blog posts
- **WHEN** crawling completes with N new blog posts
- **THEN** insert N documents into simon_willison_blog collection
- **AND** log "N simon willison blog inserted" with the count

#### Scenario: Skip duplicate blog posts
- **WHEN** a blog post with the same id already exists in the collection
- **THEN** skip insertion of the duplicate post
- **AND** log only the count of newly inserted posts

### Requirement: Generate daily news report for Simon Willison blog
The system SHALL generate a daily news report section for Simon Willison Blog, listing blog posts ordered by publication date from newest to oldest.

#### Scenario: Generate daily news report section
- **WHEN** the daily news reporter runs
- **THEN** create a section titled "## Simon Willison Blog"
- **AND** query the simon_willison_blog collection for posts from the last 7 days
- **AND** order results by created_at in descending order
- **AND** format each post as a Markdown link with the publication date
- **AND** log "Simon Willison Blog count: N" with the count

#### Scenario: Format blog post entry in report
- **WHEN** formatting a blog post for the report
- **THEN** display as "- [YYYY-MM-DD](url) title"
- **WHERE** YYYY-MM-DD is the publication date, url is the full post URL, and title is the post title

### Requirement: Enable/disable crawler via configuration
The system SHALL allow enabling or disabling the Simon Willison blog crawler through the enabled_topics configuration in cyber_news_config.yaml.

#### Scenario: Enable crawler via configuration
- **WHEN** enabled_topics contains "simon_willison_blog"
- **THEN** execute the Simon Willison blog crawler during the crawl phase

#### Scenario: Disable crawler via configuration
- **WHEN** enabled_topics is set but does not contain "simon_willison_blog"
- **THEN** skip the Simon Willison blog crawler
- **AND** log "Skipping simon_willison_blog (not in enabled_topics)"
