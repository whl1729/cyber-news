## Why

Yohei Nakajima is a prominent AI researcher and entrepreneur known for his work on autonomous AI agents (BabyAGI). Adding his blog to the news aggregator will provide valuable insights into AI agent development, autonomous systems, and emerging AI trends.

## What Changes

- Add new crawler for Yohei Nakajima's Blog (https://yoheinakajima.com/blog/)
- Add new reporter to display Yohei Nakajima's blog posts in daily news reports
- Register the new crawler in the AI crawler module
- Add configuration for the new topic in enabled_topics

## Capabilities

### New Capabilities
- `yohei-nakajima-blog-crawler`: Crawls blog posts from Yohei Nakajima's website, extracts title, URL, publication date, and stores them in MongoDB
- `yohei-nakajima-blog-reporter`: Generates formatted sections in daily news reports showing Yohei Nakajima's latest blog posts

### Modified Capabilities
<!-- No existing capabilities are being modified -->

## Impact

- New files: `news/crawler/ai/yohei_nakajima_blog_crawler.py`
- New files: `news/reporter/yohei_nakajima_blog_reporter.py`
- Modified: `news/crawler/ai/ai_crawler.py` (register new crawler)
- Modified: `news/reporter/news_reporter.py` (register new reporter)
- Modified: `config/cyber_news_config.yaml` (add to enabled_topics)
- MongoDB: New collection `yohei_nakajima_blog` will be created
