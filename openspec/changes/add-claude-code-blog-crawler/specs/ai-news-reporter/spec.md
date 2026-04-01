## ADDED Requirements

### Requirement: AI 资讯报告展示
系统 SHALL 在每日和每周报告中展示 AI 相关资讯。

#### Scenario: 每日报告包含 Claude Code 博客
- **WHEN** 生成每日新闻报告
- **THEN** 报告包含当天的 Claude Code 博客文章列表

#### Scenario: 每周报告包含 Claude Code 博客
- **WHEN** 生成每周新闻报告
- **THEN** 报告包含本周的 Claude Code 博客文章列表

#### Scenario: 文章信息完整展示
- **WHEN** 展示 Claude Code 博客文章
- **THEN** 显示标题、时间、Category、Product 等信息
