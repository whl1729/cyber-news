# Claude Code 提示词

## 2026-04-01

### 支持爬取 Claude Code 博客

v1.4:

请继续完善 Claude Code 的爬取逻辑：

目前只爬取了首页默认加载的博客信息，请改为爬取所有信息。
提示：每点击一次 `View more` 按钮就能多加载一些博客

v1.3:

请分析以下问题并修复：

我查看 /Users/along/src/cyber-daily-news/content/posts/2026-04-01.md，
发现 claude code blog 数据残缺，比如显示的第一篇博客是 2026-03-12 的，而事实上官网的最新博客是 2026-03-30 的

claude_code_blog_crawler

v1.2:

请修改：

1. 请修改 Claude Code Blog 的路径为 `https://claude.com/blog`
2. 我下载了 Claude Code Blog 的主页文件，保存在 `~/Downloads/Blog_Claude.html`，请据此检查你的解析过程是否正确

v1.1:

请根据以下要求修改 proposal 文档：

1. 只需要在 daily_news_reporter.py 添加 AI 资讯章节，不需要在 weekly_news_reporter.py 中添加
2. 请注意新增的 crawler 仍然需要使用 map 结构来支持配置开关，请将这个需求写入相关 Claude 文档，使得每次开发时都能遵守这个规则

v1.0:

请帮忙增加爬取 Claude Code 博客的功能：

1. 请在 @news/crawler 增加一个模块 ai，这个模块中都是爬取 AI 相关资讯
2. 请在 @news/crawler/ai 中支取爬取 Claude Code 博客，只需爬取标题、时间、Category、Product 等基本信息
3. 请在 @news/reporter 中增加显示 Claude Code 博客信息
4. 爬取 Claude Code 时需要使用代理

## 2026-03-28

### 支持爬取「机器之心」

v1.0:

请帮忙修复 @news/crawler/tech_news/jiqizhixin_crawler.py，目前无法爬取「机器之心」网站的文章了，请分析原因并修复。

### 支持配置 crawler 开关

v1.4:

你的实现仍然有问题，每种 language 会有多个话题。我希望在每种 language 的 claw 里面，也修改为：

1. 定义一个 map，key 为话题，value 为对应的 crawler
2. 遍历配置文件中的话题，从 map 中获取对应的 crawler，调用其 claw 方法
3. 这样更简洁和优雅

v1.3:

请帮忙修改 @news/crawler/language/ 模块：

1. language_crawler.py 直接调用各个 language 的 clawer 的 craw 方法
2. 各个 language 的 craw 方法里面实现根据配置开关来调用子 clawer 的 craw 方法

v1.2:

你漏改 @news/crawler/self_driving/ 了,请修改

v1.1:

请修改配置开关的实现方式：

1. 目前你的实现方式，每增加一个话题，就需要增加几行 `if/else` 代码，不够优雅
2. 我希望改成：
   1. 定义一个 map，key 为话题，value 为对应的 crawler
   2. 遍历配置文件中的话题，从 map 中获取对应的 crawler，调用其 claw 方法
   3. 这样更简洁和优雅

v1.0:

请帮我增加根据配置开关来决定是否爬取每个主题的新闻：

1. 一个新闻主题对应一个 crawler，比如 ruanyifeng_weekly 和 github_trending 分别是一个主题
2. 请在 @config/cyber_news_config.yaml 增加配置爬取的新闻主题列表，不在列表内的新闻不再爬取

## 2026-03-27

### 修复大部分网站爬虫失败的问题

请帮我分析以下网站爬虫失败的原因并修复：

- github
  - github_notification
  - github_received_event
  - github_trending
- language
  - cpp
    - isocpp_blog
  - go
    - go_blog
    - go_news
    - go_weekly
  - python
    - pycoder_weekly
    - python_insider
  - rust
    - rust_blog
    - rust_weekly
- tech_news
  - geekpark
  - hacker_news
  - infoq
  - jiqizhixin
  - new_stack
  - xinzhiyuan
