## ADDED Requirements

### Requirement: 爬取 OpenAI News 列表页
系统 SHALL 通过 HTTP GET 请求爬取 `https://openai.com/zh-Hans-CN/news/`，不使用代理，解析页面中的新闻条目，存入 MongoDB `openai_news` collection。

#### Scenario: 成功爬取并存储
- **WHEN** 请求 OpenAI News 页面返回 HTTP 200
- **THEN** 解析页面中所有带 `<time dateTime>` 的新闻条目，存入 MongoDB，记录插入数量

#### Scenario: 请求失败
- **WHEN** 请求 OpenAI News 页面返回非 200 状态码或网络异常
- **THEN** 记录错误日志，返回 False，不插入任何数据

### Requirement: 解析新闻条目字段
系统 SHALL 从页面 HTML 中解析每条新闻的标题、URL 和发布日期。

#### Scenario: 解析标准格式新闻条目
- **WHEN** 页面包含 `<a aria-label="...">` 和 `<time dateTime="YYYY-MM-DDTHH:MM">` 标签
- **THEN** 提取标题（aria-label 第一个 ` - ` 分隔前的部分）、URL（`https://openai.com/zh-Hans-CN` + href）、created_at（dateTime 前10位 `YYYY-MM-DD`）

#### Scenario: 缺少 time 标签的条目
- **WHEN** 某个新闻条目缺少 `<time dateTime>` 标签
- **THEN** 跳过该条目，不引发异常，记录 warning 日志

### Requirement: 通过 enabled_topics 控制爬虫开关
系统 SHALL 支持通过 `enabled_topics` 配置项控制 `openai_news` 爬虫是否运行。

#### Scenario: enabled_topics 为 None（运行全部）
- **WHEN** `get_enabled_topics()` 返回 None
- **THEN** openai_news 爬虫正常执行

#### Scenario: enabled_topics 包含 openai_news
- **WHEN** `get_enabled_topics()` 返回包含 `"openai_news"` 的列表
- **THEN** openai_news 爬虫正常执行

#### Scenario: enabled_topics 不包含 openai_news
- **WHEN** `get_enabled_topics()` 返回不含 `"openai_news"` 的列表
- **THEN** 跳过 openai_news 爬虫，记录 info 日志

### Requirement: 在每日报告中展示 OpenAI News
系统 SHALL 在每日新闻报告中包含 OpenAI News 区块，按 `created_at` 降序排列。

#### Scenario: 有新闻数据时
- **WHEN** MongoDB `openai_news` collection 中有过去24小时内的数据
- **THEN** 报告包含 `## OpenAI News` 区块，条目按发布时间由新到旧排列

#### Scenario: 无新闻数据时
- **WHEN** MongoDB `openai_news` collection 中无过去24小时内的数据
- **THEN** 报告不包含 `## OpenAI News` 区块
