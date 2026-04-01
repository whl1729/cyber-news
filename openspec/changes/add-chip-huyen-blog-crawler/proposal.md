## Why

Chip Huyen is a prominent AI engineer and author whose blog covers practical AI system design, MLOps, and LLM engineering. Adding her blog to the crawler expands coverage of high-quality technical AI content alongside existing sources like Karpathy Blog and OpenAI News.

## What Changes

- Add `ChipHuyenBlogCrawler` in `news/crawler/ai/chip_huyen_blog_crawler.py`
- Register `chip_huyen_blog` topic in `news/crawler/ai/ai_crawler.py`
- Add `DailyNewsReporter("Chip Huyen Blog", "chip_huyen_blog", order_by="created_at")` to `news/reporter/news_reporter.py`
- Add `chip_huyen_blog` to `config/cyber_news_config.yaml` enabled_topics

## Capabilities

### New Capabilities
- `chip-huyen-blog`: Crawl blog posts from `https://huyenchip.com/blog/`, storing title, URL, and publish date; report them sorted by `created_at` descending

### Modified Capabilities
- `ai-crawler`: Register new `chip_huyen_blog` topic in the AI crawler dispatcher

## Impact

- New file: `news/crawler/ai/chip_huyen_blog_crawler.py`
- Modified: `news/crawler/ai/ai_crawler.py` (add import + dict entry)
- Modified: `news/reporter/news_reporter.py` (add DailyNewsReporter entry)
- Modified: `config/cyber_news_config.yaml` (add enabled topic)
- New MongoDB collection: `chip_huyen_blog`
