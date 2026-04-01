## Context

项目已有 `news/crawler/ai/` 目录，包含 `claude_code_blog_crawler.py` 作为参考实现。OpenAI News 页面（`https://openai.com/zh-Hans-CN/news/`）是 Next.js SSR 渲染，静态 HTML 中包含两种可解析结构：
1. `<a aria-label="标题 - 分类 - 日期">` 属性
2. `<time dateTime="ISO_DATE">` 标签

报告器已有 `DailyNewsReporter` 类支持按 `created_at` 排序，Claude Code Blog 已使用相同模式。

## Goals / Non-Goals

**Goals:**
- 新增 `openai_news_crawler.py`，解析 OpenAI News 列表页，存入 MongoDB `openai_news` collection
- 在 `ai_crawler.py` 中注册��虫，支持 `enabled_topics` 开关
- 在 `news_reporter.py` 的 `report_daily_news()` 中增加 OpenAI News 区块，按 `created_at` 排序
- 不使用代理

**Non-Goals:**
- 不爬取文章详情页内容
- 不支持分页（仅爬取首页列表）
- 不使用 Selenium（静态 HTML 已包含足够数据）

## Decisions

### 解析策略：使用 aria-label 属性 + time 标签

OpenAI News 页面使用 Next.js，主要内容在静态 HTML 中通过 `aria-label` 编码在 `<a>` 标签上，格式为 `"标题 - 分类 - 日期"`。同时 `<time dateTime="...">` 标签提供 ISO 格式日期。

**选择 `<time dateTime>` 解析日期**，原因：ISO 格式（`2026-03-31T13:00`）可直接截取前10位得到 `YYYY-MM-DD`，无需依赖 `timelib` 的本地化日期解析，更健壮。

**选择 `aria-label` 解析标题**，原因：比 `<time>` 近邻的文本节点更稳定，不依赖 CSS 类名（类名易随构建变更）。

备选方案（已排除）：
- 解析 `__next_f.push` 内联 JSON：数据结构复杂，需要处理分块传输编码，脆弱
- 使用 CSS 类名定位：Next.js 构建哈希类名会频繁变化

### 文章 URL 构造

从 `aria-label` 关联 `<a>` 的 `href`（格式 `/index/<slug>`），拼接 `https://openai.com/zh-Hans-CN` 前缀。

### 去重字段

使用 `id` = 文章标题，与其他爬虫保持一致，`mongo.insert_many_new(name, "id", ...)` 自动去重。

### 报告位置

插入在 `Claude Code Blog` 之后，与其同属 AI 类来源，便于阅读对比。

## Risks / Trade-offs

- **页面结构变更** → 如果 OpenAI 修改 `aria-label` 格式或 `<time>` 标签，解析会失败。缓解：日志中会记录解析数量，0条时可排查。
- **中文日期在 aria-label 中** → `aria-label` 中的日期为中文（如 `2026年3月31日`），不用于解析，只用于人工核对。实际日期取自 `<time dateTime>`，无此风险。
- **无代理访问** → 国内网络直连 `openai.com` 可能失败。缓解：用户明确表示不需要代理，符合其网络环境。
