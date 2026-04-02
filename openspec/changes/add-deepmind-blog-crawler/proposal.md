## Why

DeepMind (now Google DeepMind) is a leading AI research lab known for breakthroughs like AlphaGo, AlphaFold, and Gemini. Adding their blog to the news aggregator will provide insights into cutting-edge AI research, model developments, and applications from one of the most influential AI organizations.

## What Changes

- Add new crawler for DeepMind Blog (https://deepmind.google/blog/)
- Add new reporter to display DeepMind blog posts in daily news reports
- Register the new crawler in the AI crawler module
- Add configuration for the new topic in enabled_topics

## Capabilities

### New Capabilities
- `deepmind-blog-crawler`: Crawls blog posts from DeepMind's website, extracts title, URL, publication date, and stores them in MongoDB
- `deepmind-blog-reporter`: Generates formatted sections in daily news reports showing DeepMind's latest blog posts

### Modified Capabilities
<!-- No existing capabilities are being modified -->

## Impact

- New files: `news/crawler/ai/deepmind_blog_crawler.py`
- New files: `news/reporter/deepmind_blog_reporter.py`
- Modified: `news/crawler/ai/ai_crawler.py` (register new crawler)
- Modified: `news/reporter/news_reporter.py` (register new reporter)
- Modified: `config/cyber_news_config.yaml` (add to enabled_topics)
- MongoDB: New collection `deepmind_blog` will be created
