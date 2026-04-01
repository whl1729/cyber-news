## 1. 新增 OpenAI News 爬虫

- [x] 1.1 新建 `news/crawler/ai/openai_news_crawler.py`，实现 `OpenAINewsParser`，使用 `<a aria-label>` + `<time dateTime>` 解析新闻条目
- [x] 1.2 实现 `crawl()` 函数，调用 `web_crawler.crawl()`，传入 `disable_proxy=True`，collection 名为 `openai_news`

## 2. 注册爬虫

- [x] 2.1 在 `news/crawler/ai/ai_crawler.py` 中 import `openai_news_crawler`，并在 `crawlers` dict 中添加 `"openai_news": openai_news_crawler`

## 3. 增加报告区块

- [x] 3.1 在 `news/reporter/news_reporter.py` 的 `report_daily_news()` 中，在 Claude Code Blog 之后添加 `DailyNewsReporter("OpenAI News", "openai_news", order_by="created_at")`
