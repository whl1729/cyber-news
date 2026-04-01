## 1. 创建 AI 爬虫模块结构

- [x] 1.1 创建 `news/crawler/ai/__init__.py` 文件
- [x] 1.2 创建 `news/crawler/ai/claude_code_blog_crawler.py` 文件

## 2. 实现 Claude Code 博客爬虫

- [x] 2.1 实现爬取 Claude Code 博客的核心逻辑（标题、时间、Category、Product）
- [x] 2.2 添加代理支持（使用 PROXY_URL 环境变量）
- [x] 2.3 实现数据存储到 MongoDB（collection: claude_code_blog）
- [x] 2.4 添加去重逻辑避免重复插入

## 3. 注册 AI 爬虫到主协调器

- [x] 3.1 在 `news/crawler/news_crawler.py` 中导入并调用 AI 爬虫

## 4. 添加报告展示功能

- [x] 4.1 在 `news/reporter/news_reporter.py` 中的 `report_daily_news()` 添加 AI 资讯展示

## 5. 测试验证

- [ ] 5.1 测试爬虫能否正常爬取 Claude Code 博客
- [ ] 5.2 验证代理配置是否生效
- [ ] 5.3 验证报告中是否正确显示 AI 资讯
