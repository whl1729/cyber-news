## Why

Harrison Chase is a notable AI/LLM developer who writes about coding agents, AI applications, and practical AI implementation. His blog on blog.langchain.com features frequent posts on agent-based systems, LLM workflows, and real-world AI deployment patterns. Adding his blog as a news source will enrich the AI section with valuable insights on engineering with AI agents.

## What Changes

- Add `harrison_chase_blog_crawler.py` to `news/crawler/ai/` to scrape blog posts from blog.langchain.com/author/harrison/
- Add Harrison Chase Blog reporter to `news/reporter/news_reporter.py` to include blog posts in daily news reports
- Register the new crawler in the AI crawler coordinator (`news/crawler/ai/ai_crawler.py`)

## Capabilities

### New Capabilities

- `harrison-chase-blog`: Crawl and report blog posts from Harrison Chase's Weblog (blog.langchain.com/author/harrison/)

### Modified Capabilities

None

## Impact

- New collection `harrison_chase_blog` in MongoDB
- New section "Harrison Chase Blog" in daily news reports
- Uses existing infrastructure (WebParser, DailyNewsReporter, MongoDB)
- No external dependencies added
