## Why

Three high-signal AI/engineering blogs are not yet tracked: Cursor's engineering blog (key AI IDE updates), Martin Fowler's "Exploring Gen AI" series (practical software engineering with AI), and Lance Martin's blog (LangChain team member, agents/context engineering). Adding them enriches the daily news report with relevant AI tooling and engineering content.

## What Changes

- Add `cursor_blog_crawler.py` to `news/crawler/ai/` — scrapes https://cursor.com/blog
- Add `martin_fowler_gen_ai_crawler.py` to `news/crawler/ai/` — scrapes the "Exploring Gen AI" series index at https://martinfowler.com/articles/exploring-gen-ai.html
- Add `lance_martin_blog_crawler.py` to `news/crawler/ai/` — scrapes https://rlancemartin.github.io
- Register all three crawlers in `news/crawler/ai/ai_crawler.py`
- Register all three reporters in `news/reporter/news_reporter.py`
- Add all three topics to `config/cyber_news_config.yaml`

## Capabilities

### New Capabilities

- `cursor-blog-crawler`: Crawl and report Cursor blog posts from cursor.com/blog
- `martin-fowler-gen-ai-crawler`: Crawl and report Martin Fowler's "Exploring Gen AI" series articles
- `lance-martin-blog-crawler`: Crawl and report Lance Martin's GitHub Pages blog posts

### Modified Capabilities

<!-- None — no existing spec-level behavior changes -->

## Impact

- New files: 3 crawler files in `news/crawler/ai/`
- Modified files: `news/crawler/ai/ai_crawler.py`, `news/reporter/news_reporter.py`, `config/cyber_news_config.yaml`
- New MongoDB collections: `cursor_blog`, `martin_fowler_gen_ai`, `lance_martin_blog`
- No new dependencies required (BeautifulSoup + requests already available)
