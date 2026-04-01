## Context

当前新闻聚合系统已支持多个类别的爬虫（blog, github, language, self_driving, tech_news），需要扩展以支持 AI 领域资讯。Claude Code 博客是重要的 AI 工具资讯来源，需要定期爬取。

现有架构：
- 爬虫按类别组织在 `news/crawler/` 下
- 每个类别有独立的模块和 `__init__.py` 协调子爬虫
- 主协调器 `news_crawler.py` 按顺序调用各类别爬虫
- 报告器从 MongoDB 读取数据生成 Markdown 报告

## Goals / Non-Goals

**Goals:**
- 新增 AI 类别爬虫模块，支持 Claude Code 博客爬取
- 在每日/每周报告中展示 AI 资讯
- 使用代理访问 Claude Code 博客

**Non-Goals:**
- 不支持其他 AI 博客（如 OpenAI, Gemini）- 可后续扩展
- 不爬取博客文章全文，仅基本信息

## Decisions

### 1. 模块结构
遵循现有模式创建 `news/crawler/ai/` 模块：
- `__init__.py` - 协调 AI 类别下的所有爬虫
- `claude_code_blog_crawler.py` - Claude Code 博客爬虫实现

**Rationale**: 保持与现有架构一致，便于后续添加其他 AI 资讯源。

### 2. 爬取方式
使用 requests + 代理访问 Claude Code 博客 RSS/API。

**Alternatives considered**:
- Selenium: 过重，Claude Code 博客可能有 RSS 或静态页面
- 直接访问: 可能需要代理才能访问

**Rationale**: 优先尝试轻量级方案，如需 JavaScript 渲染再考虑 Selenium。

### 3. 数据存储
MongoDB collection 命名: `claude_code_blog`

**Rationale**: 遵循现有命名规范（如 `hacker_news`, `github_trending`）。

### 4. 报告展示
在 `DailyNewsReporter` 和 `WeeklyNewsReporter` 中添加 AI 资讯章节。

**Rationale**: 与其他类别资讯保持一致的展示方式。

## Risks / Trade-offs

- **[Risk] Claude Code 博客结构变化** → 需要定期检查爬虫是否正常工作
- **[Risk] 代理不稳定** → 添加重试机制和错误日志
- **[Trade-off] 仅爬取基本信息** → 减少存储和处理开销，但可能需要用户点击链接查看详情
