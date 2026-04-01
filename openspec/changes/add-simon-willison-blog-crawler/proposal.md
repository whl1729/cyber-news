## Why

Simon Willison is a prominent developer known for his work on Datasette, Django, and AI/LLM tools. His weblog (simonwillison.net) features frequent posts about SQLite, AI, programming, and data visualization. Adding his blog as a news source will enrich the AI section with valuable insights on practical development and AI applications.

## What Changes

- Add `simon_willison_blog_crawler.py` to `news/crawler/ai/` to scrape blog posts from simonwillison.net/entries/
- Add Simon Willison Blog reporter to `news/reporter/news_reporter.py` to include blog posts in daily news reports
- Register the new crawler in the AI crawler coordinator (`news/crawler/ai/ai_crawler.py`)

## Capabilities

### New Capabilities

- `simon-willison-blog`: Crawl and report blog posts from Simon Willison's Weblog (simonwillison.net/entries/)

### Modified Capabilities

None

## Impact

- New collection `simon_willison_blog` in MongoDB
- New section "Simon Willison Blog" in daily news reports
- Uses existing infrastructure (WebParser, DailyNewsReporter, MongoDB)
- No external dependencies added
