# Claude Code 提示词

## 2026-04-04

v1.1:

但是我的 MongoDB 数据库中，历史数据还是原来的格式，这个问题仍然存在，如何解决？

v1.0:

请帮我修复 1 个问题：

今天我访问 cyber-daily-news 网站，发现网站上会显示很多旧博客。理论上，一天以前的博客不应再显示。
经过初步分析，我已找出原因（如下所述），请修改。

@news/crawler/ai 的很多 crawler 的 `crawled_at` 字段没遵守 @news/util/timelib.py 的 `now2()` 的格式，导致 @news/reporter/daily_news_reporter.py 的 report 函数的日期比较出错了。

## 2026-04-02

### 爬取 3 个 AI 博客

请帮忙增加爬取以下博客的功能：

1. 请在 @news/crawler/ai 中增加对应的 crawler
2. 请在 @news/reporter 中增加对应的 reporter

- https://cursor.com/cn/blog
- https://martinfowler.com/articles/exploring-gen-ai.html
- https://rlancemartin.github.io

### 爬取其他 AI 博客

请帮忙增加爬取以下博客的功能：

1. 请在 @news/crawler/ai 中增加对应的 crawler
2. 请在 @news/reporter 中增加对应的 reporter

- [BaoYu Blog][21]
- [Sam Altman Blog][4]
- [Mario Zechner][15]
- [David Heinemeier Hansson][9]
- [Armin Ronacher's Thoughts and Writings][10]
- [antirez][11]
- [Ryan Dahl][12]
- [The Pragmatic Engineer][13]
- [sean goedecke][16]
- [Philipp Schmid][17]
- [Matt Shumer][18]
- [Bassim Eledath][19]
- [Rob Zolkos][22]
- [Chris Gregori][23]
- [Addy Osmani][24]
- [Uwe Friedrichsen][25]
- [One Useful Thing][26]
- [Han, Not Solo][27]

  [4]: https://blog.samaltman.com/
  [8]: https://simonwillison.net
  [9]: https://world.hey.com/dhh
  [10]: https://lucumr.pocoo.org
  [11]: https://antirez.com/latest/0
  [12]: https://tinyclouds.org
  [13]: https://newsletter.pragmaticengineer.com
  [15]: https://mariozechner.at
  [16]: https://www.seangoedecke.com
  [17]: https://www.philschmid.de
  [18]: https://shumer.dev/blog
  [19]: https://www.bassimeledath.com/blog
  [21]: https://baoyu.io/
  [22]: https://www.zolkos.com/
  [23]: https://www.chrisgregori.dev/
  [24]: https://addyosmani.com/blog/
  [25]: https://www.ufried.com/
  [26]: https://www.oneusefulthing.org
  [27]: https://leehanchung.github.io/blogs/

### 爬取 Hugging Face Blog

v1.0:

请帮忙增加爬取 Hugging Face Blog 的功能：

1. 爬取的网站地址为：`https://huggingface.co/blog`
3. 请在 @news/crawler/ai 中增加对应的 crawler
4. 请在 @news/reporter 中增加对应的 reporter

### 爬取 DeepMind Blog

v1.0:

请帮忙增加爬取 DeepMind Blog 的功能：

1. 爬取的网站地址为：`https://deepmind.google/blog/`
3. 请在 @news/crawler/ai 中增加对应的 crawler
4. 请在 @news/reporter 中增加对应的 reporter

### 爬取 Harrison Chase's Blog

v1.0:

请帮忙增加爬取 Yohei Nakajima's Blog 的功能：

1. 爬取的网站地址为：`https://yoheinakajima.com/blog/`
3. 请在 @news/crawler/ai 中增加对应的 crawler
4. 请在 @news/reporter 中增加对应的 reporter

### 支持 topic 参数

v1.2:

你的修改仍然有问题：请将 @news/news_generator.py 的解析参数的逻辑全部移到 @news/util/argparser.py，包括解析 `-t` 参数。
@news/util/argparser.py 这个模块就是用来解析所有输入参数的啊，能不能专业一些？

v1.1：

你的修改方法有问题，这样会导致 logger.py 无法使用输入的日志登记参数，建议修改为：

保留在 @news/util/argparser.py 中解析输入参数，@news/news_generator.py 改为调用 @news/util/argparser.py 的函数即可

v1.0:

请帮忙实现一个功能：

#### 需求描述

我希望程序中支持一个输入参数 `-t <topic>`，当用户输入该参数时，则只爬取这个 topic 的数据。

#### 方案描述

建议修改 @news/util/configer.py 的 get_enabled_topics 的逻辑：
当用户输入 topic 参数时，该函数直接返回用户输入的 topic 即可

## 2026-04-01

### 爬取 Harrison Chase's Blog

v1.2:

为什么你无法提取日信息?我看博客中开头是有完整的日期信息的,比如"MAR 10, 2026"

v1.1:

请帮忙修复一个问题：

生成的 Markdown 文档中，Harrison Chase 的每篇博客都是 2026-04-01，不是真实时间，请修改。

v1.0:

请帮忙增加爬取 Harrison Chase’s Weblog 的功能：

1. 爬取的网站地址为：`https://blog.langchain.com/author/harrison/`
2. 我手动下载的离线 HTML 路径为：`/Users/along/Downloads/Harrison_Chase_Blog.html`
3. 请在 @news/crawler/ai 中增加对应的 crawler
4. 请在 @news/reporter 中增加对应的 reporter

### 爬取 Simon Willison’s Weblog

请帮忙增加爬取 Simon Willison’s Weblog 的功能：

1. 爬取的网站地址为：`https://simonwillison.net/entries/`
2. 我手动下载的离线 HTML 路径为：`/Users/along/Downloads/Simon_Willison_Weblog.html`
3. 请在 @news/crawler/ai 中增加对应的 crawler
4. 请在 @news/reporter 中增加对应的 reporter

### 爬取 Sebastian Raschka Blog

请帮忙增加爬取 Chip Huyen blog 的功能：

1. 爬取的网站地址为：`https://sebastianraschka.com`
2. 我手动下载的离线 HTML 路径为：`/Users/along/Downloads/Sebastian_Raschka_Blog.html`
3. 请在 @news/crawler/ai 中增加对应的 crawler
4. 请在 @news/reporter 中增加对应的 reporter

### 爬取 Chip Huyen Blog

v1.0:

请帮忙增加爬取 Chip Huyen blog 的功能：

1. 爬取的网站地址为：`https://huyenchip.com/blog/`
2. 我手动下载的离线 HTML 路径为：`/Users/along/Downloads/Chip_Huyen_Blog.html`
3. 请在 @news/crawler/ai 中增加对应的 crawler
4. 请在 @news/reporter 中增加对应的 reporter

### 爬取 Andrej Karpathy blog

v1.1:

请在 @config/cyber_news_config.yaml 的 `enabled_topics` 中新增当前 topic，并将这个操作写入 CLAUDE.md

v1.0:

请帮忙增加爬取 Andrej Karpathy blog 的功能：

1. 爬取的网站地址为：`https://karpathy.github.io`
2. 我手动下载的离线 HTML 路径为：`/Users/along/Downloads/Andrej_Karpathy_blog.html`
3. 请在 @news/crawler/ai 中支持爬取 Andrej Karpathy blog
4. 请在 @news/reporter 中增加显示 Andrej Karpathy blog

### 支持爬取 OpenAI News

v1.1:

请测试是否能爬取到新闻条目，以及是否能正确显示在生成的新闻报告中，并且新闻报告中是否按照 created_at 时间排序。
请将这些操作写入 Claude 相关文档，以便自动执行。

测试步骤（自动执行）：

1. 运行爬虫，验证能爬取到新闻条目：
   ```bash
   ./script/run.sh -p news/crawler/ai/openai_news_crawler.py -l debug
   # 预期：日志中显示 "N openai news inserted"（N > 0）
   ```

2. 运行报告生成器，验证 OpenAI News 区块存在且按 created_at 降序排列：
   ```bash
   ./script/run.sh -p news/reporter/news_reporter.py -l debug
   # 预期：日志中显示 "OpenAI News count: N"（N > 0）
   # 预期：生成的 md 文件中 ## OpenAI News 区块条目日期由新到旧排列
   ```

3. 验证报告内容：
   ```bash
   grep -A 15 "## OpenAI News" $(ls /Users/along/src/cyber-daily-news/content/posts/*.md | tail -1)
   # 预期：显示新闻列表，日期格式 YYYY-MM-DD，从新到旧排列
   ```

4. 运行 pre-commit 检查代码规范：
   ```bash
   git add news/crawler/ai/openai_news_crawler.py news/crawler/ai/ai_crawler.py news/reporter/news_reporter.py news/util/myrequests.py requirements.txt
   pre-commit run --files news/crawler/ai/openai_news_crawler.py news/crawler/ai/ai_crawler.py news/reporter/news_reporter.py news/util/myrequests.py requirements.txt
   # 预期：所有检查通过（black, flake8, autoflake 等）
   ```

技术说明：
- OpenAI 网站使用 Cloudflare TLS 指纹检测，需用 `curl_cffi` 模拟 Chrome 指纹（已加入 requirements.txt）
- 解析逻辑：`<a aria-label="标题 - 分类 - 日期">` + `<time datetime="YYYY-MM-DDTHH:MM">` 取日期前10位
- 使用全局代理（`config["proxies"]`），同 Claude Code Blog 爬虫

v1.0:

请帮忙增加爬取 OpenAI News 的功能：

1. 爬取的网站地址为：`https://openai.com/zh-Hans-CN/news/`
2. 我手动下载的离线 HTML 路径为：`/Users/along/Downloads/OpenAI_News.html`
3. 请在 @news/crawler/ai 中支持爬取 OpenAI News
4. 请在 @news/reporter 中增加显示 OpenAI News
5. 爬取 OpenAI News 时不需要使用代理

### 支持爬取 Claude Code 博客

v1.5:

请分析以下问题并修改：

在 reporter 最终生成的 report 中，Claude Code 的博客没有按时间顺序由新到旧排序。

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
