# Claude Code 提示词

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
