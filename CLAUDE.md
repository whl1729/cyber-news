# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

Cyber News 是一个新闻聚合爬虫项目，每日从多个来源收集技术新闻并生成 Markdown 格式的报告。

**核心流程**：爬取（crawl）→ 报告（report）
- 爬虫从各个来源抓取新闻并存储到 MongoDB
- 报告器从数据库读取数据并生成每日/每周新闻报告

## 技术栈

- Python 3.10+
- MongoDB（存储爬取的新闻数据）
- Selenium（用于需要 JavaScript 渲染的网站）
- pre-commit hooks（black, flake8, commitizen）

## 常用命令

### 开发环境设置
```bash
# 安装依赖（包括 Python 包和 pre-commit hooks）
./script/install_dependencies.sh
```

### 运行程序
```bash
# 运行完整流程（爬取 + 生成报告）
./script/run.sh

# 运行特定脚本
./script/run.sh -p news/crawler/tech_news/hacker_news_crawler.py

# 指定日志级别
./script/run.sh -l debug
```

### 测试
```bash
# 运行单个测试文件
./script/test.sh test/test_hacker_news_parser.py

# 或直接使用 pytest
pytest test/test_hacker_news_parser.py
```

## 项目架构

### 目录结构
- `news/crawler/` - 爬虫实现，按主题分类
  - `blog/` - 博客爬虫（如阮一峰周刊）
  - `github/` - GitHub 相关（trending, notifications, events）
  - `language/` - 编程语言官方博客（Go, Python, Rust, C++）
  - `self_driving/` - 自动驾驶相关新闻
  - `tech_news/` - 技术媒体（Hacker News, 机器之心等）
- `news/reporter/` - 报告生成器
- `news/util/` - 工具模块（MongoDB, 日志, 配置等）
- `config/` - 配置文件
- `script/` - 运行脚本

### 核心模块

**news_generator.py**：主入口，协调爬虫和报告器
- 调用 `news_crawler.crawl()` 执行所有爬虫
- 调用 `news_reporter.report()` 生成报告

**news_crawler.py**：爬虫协调器
- 按顺序调用各类别爬虫（blog, github, language, self_driving, tech_news）
- 每个类别爬虫负责调用其子爬虫

**news_reporter.py**：报告生成器
- 生成每日新闻报告（DailyNewsReporter）
- 生成周刊报告（WeeklyNewsReporter）
- 生成个人化新闻（GitHub notifications/events）
- 输出 Markdown 格式文件

### 配置管理

配置通过环境变量和 YAML 文件管理（`news/util/configer.py`）：
- 从 `.env` 文件加载环境变量
- 从 `config/cyber_news_config.yaml` 加载基础配置
- 必需的环境变量：
  - `MONGODB_HOST`, `MONGODB_PORT`, `MONGODB_DATABASE`
  - `GITHUB_TOKEN`（用于 GitHub API）
  - `PROXY_URL`（可选，用于需要代理的爬虫）
  - `CHROMEDRIVER_PATH`（用于 Selenium）

### 数据库

使用 MongoDB 存储爬取的新闻：
- 封装在 `news/util/mongodb.py` 中
- 提供 `insert_many_new()` 方法避免重复插入
- 每个新闻源对应一个 collection

## 开发注意事项

- 新增爬虫时，需要在对应的类别爬虫文件中注册
- 新增报告器时，需要在 `news_reporter.py` 中添加
- **报告器排序**：`DailyNewsReporter` 默认按 `crawled_at` 排序；对于有明确发布时间的博客类来源（如 Claude Code Blog、语言官方博客等），必须显式指定 `order_by="created_at"`，确保报告中按发布时间由新到旧排列
- 所有爬虫应继承或遵循现有爬虫的模式
- 使用 `news/util/logger.py` 进行日志记录
- 时间处理使用 `news/util/timelib.py`
- 提交代码前会自动运行 pre-commit hooks（格式化、lint 检查、commit 消息验证）

### 爬虫配置开关

每个类别爬虫文件（如 `tech_news_crawler.py`）中，子爬虫**必须**使用 `dict` 结构注册，并配合 `get_enabled_topics()` 实现按需开关。模板：

```python
from news.util.configer import get_enabled_topics
from news.util.logger import logger

def crawl():
    crawlers = {
        "topic_name": some_crawler,
        # ...
    }
    enabled_topics = get_enabled_topics()
    for topic, crawler in crawlers.items():
        if enabled_topics is None or topic in enabled_topics:
            crawler.crawl()
        else:
            logger.info(f"Skipping {topic} (not in enabled_topics)")
```

这样可以通过配置文件中的 `enabled_topics` 字段控制哪些爬虫运行，不列出则全部运行。

## 新需求开发完成后的验证步骤

每次开发完新的爬虫或报告器后，**必须**按以下步骤验证：

### 1. 运行爬虫，验证能爬取到新闻条目

```bash
./script/run.sh -p news/crawler/ai/<your_crawler>.py -l debug
# 预期：日志中显示 "N <source> inserted"（N > 0，首次运行）或 "N <source> parsed"
```

### 2. 运行报告生成器，验证新区块存在且按 created_at 降序排列

```bash
./script/run.sh -p news/reporter/news_reporter.py -l debug
# 预期：日志中显示 "<Section Title> count: N"（N > 0）
```

### 3. 验证报告内容

```bash
grep -A 10 "## <Section Title>" $(ls /Users/along/src/cyber-daily-news/content/posts/*.md | tail -1)
# 预期：显示新闻列表，日期格式 YYYY-MM-DD，从新到旧排列
```

### 4. 运行 pre-commit 检查代码规范

```bash
git add <modified files>
pre-commit run --files <modified files>
# 预期：所有检查通过（black, flake8, autoflake 等）
```

### 5. 在配置文件中注册新 topic

在 `config/cyber_news_config.yaml` 的 `enabled_topics` 列表中新增对应的 topic 名称（即爬虫 `dict` 中使用的 key）：

```yaml
enabled_topics:
  - <new_topic_name>
  # ...其他已有 topics
```

不注册则该爬虫不会在完整流程中运行。
