## Why

多个网站爬虫出现失败，影响了新闻聚合系统的数据完整性。涉及 GitHub、编程语言官方博客、技术媒体等 16 个爬虫源，需要系统性地诊断失败原因并修复，确保每日新闻报告的数据质量。

## What Changes

- 诊断并修复 GitHub 类爬虫（github_notification, github_received_event, github_trending）
- 修复编程语言官方博客爬虫：
  - C++: isocpp_blog
  - Go: go_blog, go_news, go_weekly
  - Python: pycoder_weekly, python_insider
  - Rust: rust_blog, rust_weekly
- 修复技术媒体爬虫：geekpark, hacker_news, infoq, jiqizhixin, new_stack, xinzhiyuan
- 增强爬虫的错误处理和日志记录
- 添加爬虫健康检查机制

## Capabilities

### New Capabilities
- `crawler-health-check`: 爬虫健康检查和监控机制，用于及时发现和报告爬虫失败
- `error-recovery`: 统一的错误恢复策略，包括重试机制和降级处理

### Modified Capabilities
<!-- 暂无现有 capability 的需求变更 -->

## Impact

- 影响的代码模块：
  - `news/crawler/github/` - 3 个爬虫文件
  - `news/crawler/language/` - 8 个爬虫文件（跨 4 个语言目录）
  - `news/crawler/tech_news/` - 6 个爬虫文件
- 可能需要更新的依赖：Selenium, requests, BeautifulSoup
- 影响的数据库 collections：对应各个爬虫源的 MongoDB collections
- 影响的报告生成：修复后将恢复完整的每日新闻报告数据
