## Why

扩展新闻聚合系统以覆盖 AI 领域资讯，特别是 Claude Code 博客内容。这将为用户提供 AI 工具和技术的最新动态。

## What Changes

- 新增 `news/crawler/ai/` 模块用于爬取 AI 相关资讯
- 实现 Claude Code 博客爬虫，抓取标题、时间、Category、Product 等信息
- 在报告生成器中添加 AI 资讯展示功能
- 配置代理支持以访问 Claude Code 博客

## Capabilities

### New Capabilities
- `ai-news-crawler`: AI 资讯爬虫模块，包含 Claude Code 博客爬取功能
- `ai-news-reporter`: AI 资讯报告生成器，在每日/每周报告中展示 AI 相关内容

### Modified Capabilities
<!-- No existing capabilities are being modified -->

## Impact

- 新增文件：`news/crawler/ai/__init__.py`, `news/crawler/ai/claude_code_blog_crawler.py`
- 修改文件：`news/crawler/news_crawler.py`（注册 AI 爬虫）
- 修改文件：`news/reporter/daily_news_reporter.py`（添加 AI 资讯展示）
- MongoDB：新增 collection 用于存储 Claude Code 博客数据
- 依赖代理配置（`PROXY_URL` 环境变量）
