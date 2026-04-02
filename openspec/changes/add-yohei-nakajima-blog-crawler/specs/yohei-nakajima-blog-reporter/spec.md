## ADDED Requirements

### Requirement: Generate daily news section for Yohei Nakajima's blog
The system SHALL generate a formatted section in the daily news report displaying Yohei Nakajima's latest blog posts.

#### Scenario: Create report section
- **WHEN** generating the daily news report
- **THEN** it SHALL create a section titled "Yohei Nakajima Blog"
- **THEN** it SHALL retrieve blog posts from the `yohei_nakajima_blog` MongoDB collection

#### Scenario: Display blog posts ordered by publication date
- **WHEN** displaying blog posts
- **THEN** they SHALL be ordered by `created_at` field in descending order (newest first)
- **THEN** each post SHALL display the title as a clickable link
- **THEN** each post SHALL display the publication date in YYYY-MM-DD format

### Requirement: Follow existing reporter patterns
The reporter SHALL follow the same implementation patterns as other blog reporters in the `news/reporter/` directory.

#### Scenario: Use DailyNewsReporter base class
- **WHEN** implementing the reporter
- **THEN** it SHALL inherit from `DailyNewsReporter`
- **THEN** it SHALL specify `order_by="created_at"` to sort by publication date
- **THEN** it SHALL use the `yohei_nakajima_blog` collection name

#### Scenario: Format output as Markdown
- **WHEN** generating the report section
- **THEN** it SHALL format output as Markdown
- **THEN** it SHALL use the format: `- [title](url) (YYYY-MM-DD)`
- **THEN** it SHALL log the count of blog posts included

### Requirement: Register in news reporter
The reporter SHALL be registered in the main news reporter module to be included in daily reports.

#### Scenario: Add to news_reporter.py
- **WHEN** the daily report is generated
- **THEN** the Yohei Nakajima Blog reporter SHALL be called
- **THEN** its output SHALL be included in the final report
