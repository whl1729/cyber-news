## Why

Sebastian Raschka is a prominent AI/LLM researcher who publishes high-quality technical blog posts on topics like LLM architectures, attention mechanisms, and inference-time scaling. Adding his blog as a news source will enrich the AI section with valuable research insights and keep users informed about cutting-edge AI developments.

## What Changes

- Add `sebastian_raschka_blog_crawler.py` to `news/crawler/ai/` to scrape blog posts from sebastianraschka.com
- Add Sebastian Raschka Blog reporter to `news/reporter/news_reporter.py` to include blog posts in daily news reports
- Register the new crawler in the AI crawler coordinator (`news/crawler/ai/ai_crawler.py`)

## Capabilities

### New Capabilities

- `sebastian-raschka-blog`: Crawl and report blog posts from Sebastian Raschka's website (sebastianraschka.com)

### Modified Capabilities

None

## Impact

- New collection `sebastian_raschka_blog` in MongoDB
- New section "Sebastian Raschka Blog" in daily news reports
- Uses existing infrastructure (WebParser, DailyNewsReporter, MongoDB)
- No external dependencies added
