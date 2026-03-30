## ADDED Requirements

### Requirement: Configuration file defines enabled topics
The system SHALL read a list of enabled crawler topics from the configuration file `config/cyber_news_config.yaml`.

#### Scenario: Configuration file contains enabled topics list
- **WHEN** the configuration file has an `enabled_topics` list
- **THEN** the system loads the list of topic names

#### Scenario: Configuration file missing enabled topics
- **WHEN** the configuration file does not have an `enabled_topics` key
- **THEN** the system SHALL enable all topics by default

### Requirement: Crawlers check topic enablement before execution
Each crawler SHALL check if its topic name is in the enabled topics list before executing.

#### Scenario: Topic is enabled
- **WHEN** a crawler's topic name is in the enabled topics list
- **THEN** the crawler executes normally

#### Scenario: Topic is disabled
- **WHEN** a crawler's topic name is not in the enabled topics list
- **THEN** the crawler is skipped and logs a message indicating it was skipped

### Requirement: Topic names match crawler identifiers
Each crawler topic SHALL have a unique identifier that matches the configuration.

#### Scenario: Topic naming convention
- **WHEN** defining topic names in configuration
- **THEN** topic names SHALL use snake_case format matching the crawler module names (e.g., `ruanyifeng_weekly`, `github_trending`, `hacker_news`, `cpp_blog`, `go_blog`, `python_blog`, `rust_blog`)
