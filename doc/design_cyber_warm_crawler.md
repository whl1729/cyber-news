# Cyber News Crawler 设计文档

## 功能设计

- 每天定时从配置的网站中抓取当天的新闻，并保存在数据库中
- 支持增删查改网站
- 支持配置过滤条件

## 数据库设计

### 数据库选型

考虑到抓取的新闻为文本型，且结构可能灵活变化，打算保存为 JSON 格式，因此选择 MongoDB。

## 数据结构设计

每条新闻应该包含以下信息：

- 新闻标题
- 摘要
- 链接
- 作者
- 发布时间
- 发布网站
- 我是否喜欢
