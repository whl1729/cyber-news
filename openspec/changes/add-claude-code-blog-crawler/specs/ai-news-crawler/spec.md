## ADDED Requirements

### Requirement: Claude Code 博客爬取
系统 SHALL 从 Claude Code 博客爬取文章信息并存储到 MongoDB。

#### Scenario: 成功爬取博客文章
- **WHEN** 爬虫运行时
- **THEN** 系统从 Claude Code 博客获取文章列表并提取标题、时间、Category、Product 信息

#### Scenario: 使用代理访问
- **WHEN** 配置了 PROXY_URL 环境变量
- **THEN** 爬虫通过代理访问 Claude Code 博客

#### Scenario: 避免重复存储
- **WHEN** 文章已存在于数据库中
- **THEN** 系统跳过该文章不重复插入

### Requirement: AI 爬虫模块注册
系统 SHALL 在主爬虫协调器中注册 AI 爬虫模块。

#### Scenario: 爬虫执行顺序
- **WHEN** 执行完整爬取流程
- **THEN** AI 爬虫在其他类别爬虫之后执行
