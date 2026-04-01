## Why

项目目前已聚合多个 AI 相关新闻来源（如 Claude Code Blog），但缺少对 OpenAI 官方新闻的跟踪。增加 OpenAI News 爬虫，可以让用户在每日报告中同时看到 OpenAI 的最新动态。

## What Changes

- 新增 `news/crawler/ai/openai_news_crawler.py`，爬取 `https://openai.com/zh-Hans-CN/news/` 的新闻列表
- 在 `news/crawler/ai/ai_crawler.py` 中注册 `openai_news` 爬虫
- 在 `news/reporter/daily_news_reporter.py` 中增加 OpenAI News 报告区块
- MongoDB 新增 `openai_news` collection 用于存储爬取数据
- 不使用代理

## Capabilities

### New Capabilities

- `openai-news-crawler`: 爬取 OpenAI 官方新闻页面，解析文章标题、URL、��布日期、分类，存入 MongoDB

### Modified Capabilities

- `ai-crawler`: 在现有 AI 类爬虫协调器中注册 openai_news 爬虫（仅实现变更，无需求变更）

## Impact

- **新增文件**：`news/crawler/ai/openai_news_crawler.py`
- **修改文件**：`news/crawler/ai/ai_crawler.py`（注册新爬虫）、`news/reporter/daily_news_reporter.py`（新增报告区块）
- **数据库**：新增 `openai_news` collection
- **依赖**：使用已有的 `requests` + `BeautifulSoup`，无新依赖
