## ADDED Requirements

### Requirement: Generate daily report section
The reporter SHALL generate a "Hugging Face Blog" section in the daily news report.

#### Scenario: Posts exist
- **WHEN** reporter runs and huggingface_blog collection has posts from last 24 hours
- **THEN** system generates section with header "## Hugging Face Blog"
- **THEN** system lists posts as numbered items: "N. [title](url) (YYYY-MM-DD)"
- **THEN** system logs "Hugging Face Blog count: N" where N > 0

#### Scenario: No recent posts
- **WHEN** reporter runs and no posts from last 24 hours exist
- **THEN** system returns empty string (no section generated)
- **THEN** system logs "Hugging Face Blog count: 0"

### Requirement: Sort by publication date descending
The reporter SHALL sort posts by created_at field in descending order (newest first).

#### Scenario: Multiple posts
- **WHEN** multiple posts exist with different created_at dates
- **THEN** system orders posts with most recent created_at first
- **THEN** report shows posts from newest to oldest

### Requirement: Inherit from DailyNewsReporter
The reporter SHALL inherit from DailyNewsReporter base class with order_by="created_at".

#### Scenario: Reporter initialization
- **WHEN** reporter is instantiated
- **THEN** system sets title="Hugging Face Blog"
- **THEN** system sets table_name="huggingface_blog"
- **THEN** system sets order_by="created_at"

### Requirement: Register in news_reporter.py
The reporter SHALL be registered in the daily reporters list.

#### Scenario: Reporter integration
- **WHEN** news_reporter.report() runs
- **THEN** system includes Hugging Face Blog reporter in daily_reporters list
- **THEN** system calls reporter.report() and includes output in final content
