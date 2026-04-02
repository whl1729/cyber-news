## ADDED Requirements

### Requirement: Crawl blog post list
The crawler SHALL fetch the blog post list from https://huggingface.co/blog and parse post metadata.

#### Scenario: Successful crawl
- **WHEN** crawler runs with topic `huggingface_blog`
- **THEN** system fetches HTML from https://huggingface.co/blog using Selenium
- **THEN** system parses blog post elements and extracts title, URL, and date
- **THEN** system logs "N huggingface blog posts parsed" where N > 0

#### Scenario: Network failure
- **WHEN** crawler cannot connect to huggingface.co
- **THEN** system logs error and returns False
- **THEN** no data is inserted into MongoDB

### Requirement: Extract post metadata
The crawler SHALL extract title, URL, and publication date from each blog post element.

#### Scenario: Complete metadata
- **WHEN** parsing a blog post with all fields present
- **THEN** system extracts title as string
- **THEN** system extracts URL (absolute or relative, converted to absolute)
- **THEN** system extracts publication date and converts to YYYY-MM-DD format

#### Scenario: Missing date
- **WHEN** parsing a blog post without a date field
- **THEN** system uses current date as fallback
- **THEN** system logs warning about missing date

### Requirement: Store in MongoDB
The crawler SHALL store parsed posts in MongoDB collection `huggingface_blog` with deduplication by `id` field.

#### Scenario: New posts
- **WHEN** crawler finds posts not in database
- **THEN** system inserts new posts with fields: id (title), url, created_at, crawled_at
- **THEN** system logs "N huggingface blog inserted" where N is count of new posts

#### Scenario: Duplicate posts
- **WHEN** crawler finds posts already in database (matching id)
- **THEN** system skips insertion
- **THEN** inserted count excludes duplicates

### Requirement: Use Selenium rendering
The crawler SHALL use Selenium for JavaScript rendering to ensure complete HTML.

#### Scenario: Selenium enabled
- **WHEN** crawler calls web_crawler.crawl()
- **THEN** system passes use_selenium=True parameter
- **THEN** system waits for page to fully render before parsing

### Requirement: Support proxy configuration
The crawler SHALL use proxy from config if available.

#### Scenario: Proxy configured
- **WHEN** config["proxies"] is set
- **THEN** crawler passes proxies parameter to web_crawler.crawl()
- **THEN** requests route through configured proxy
