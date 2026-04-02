## Why

Hugging Face is a leading AI platform and research hub, publishing frequent blog posts on model releases, research breakthroughs, and open-source tooling. Adding their blog follows the established pattern of crawling influential AI organizations' blogs alongside DeepMind, OpenAI, and others.

## What Changes

- Add `news/crawler/ai/huggingface_blog_crawler.py` to crawl `https://huggingface.co/blog`
- Register crawler in `news/crawler/ai/ai_crawler.py`
- Add `news/reporter/huggingface_blog_reporter.py` to generate daily report section
- Register reporter in `news/reporter/news_reporter.py`
- Add `huggingface_blog` to `enabled_topics` in `config/cyber_news_config.yaml`

## Capabilities

### New Capabilities

- `huggingface-blog-crawler`: Crawl blog post metadata (title, URL, date) from huggingface.co/blog and store in MongoDB collection `huggingface_blog`
- `huggingface-blog-reporter`: Generate a "Hugging Face Blog" section in the daily news report, sorted by publication date descending

### Modified Capabilities

## Impact

- New files: `news/crawler/ai/huggingface_blog_crawler.py`, `news/reporter/huggingface_blog_reporter.py`
- Modified files: `news/crawler/ai/ai_crawler.py`, `news/reporter/news_reporter.py`, `config/cyber_news_config.yaml`
- New MongoDB collection: `huggingface_blog`
- No breaking changes
