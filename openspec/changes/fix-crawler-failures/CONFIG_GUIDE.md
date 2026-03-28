# 环境配置指南

## 快速修复步骤

### 1. 修复代理配置

**问题**：代理 URL 使用了 `https://` 协议，导致 TLS in TLS 错误

**解决方法**：编辑 `news/.env` 文件，修改 `PROXY_URL`：

```bash
# 错误的配置（会导致 TLS in TLS 错误）
PROXY_URL=https://1721763:1729monocloud@global-us.link.ac.cn:152

# 正确的配置
PROXY_URL=http://1721763:1729monocloud@global-us.link.ac.cn:152
```

**原因**：即使访问 HTTPS 网站，代理协议本身也应该使用 HTTP。

### 2. 启动 MongoDB

**问题**：MongoDB 服务未运行，导致爬虫无法保存数据

**解决方法**：选择以下方式之一启动 MongoDB

#### 方式 A：使用 systemd（推荐）
```bash
sudo systemctl start mongod
sudo systemctl enable mongod  # 开机自启
```

#### 方式 B：使用 service
```bash
sudo service mongod start
```

#### 方式 C：使用 Docker
```bash
docker run -d -p 27017:27017 --name mongodb mongo
```

#### 验证 MongoDB 是否运行
```bash
# 检查服务状态
systemctl status mongod

# 或测试连接
mongo --eval "db.version()"
```

### 3. 验证 GitHub Token（可选）

如果需要使用 GitHub API 爬虫，确保设置了有效的 GitHub Token：

```bash
# 在 news/.env 文件中添加
GITHUB_TOKEN=your_github_personal_access_token
```

**获取 GitHub Token**：
1. 访问 https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 选择权限：`notifications`, `read:user`
4. 复制生成的 token 到 .env 文件

## 完整的 .env 文件示例

```bash
# MongoDB 配置
MONGODB_HOST=127.0.0.1
MONGODB_PORT=27017
MONGODB_DATABASE=newsDB

# GitHub 配置
GITHUB_USERNAME=your_username
GITHUB_TOKEN=your_github_token

# 代理配置（注意使用 http:// 而非 https://）
PROXY_URL=http://username:password@proxy-host:port

# ChromeDriver 路径（用于 Selenium）
CHROMEDRIVER_PATH=/usr/local/bin/chromedriver

# 文章输出目录
CYBER_NEWS_POST_DIR=/path/to/output/directory
```

## 测试配置

修复配置后，运行以下命令测试：

```bash
# 测试不需要 GitHub Token 的爬虫
./script/run.sh -p news/crawler/tech_news/hacker_news_crawler.py

# 测试需要 GitHub Token 的爬虫
./script/run.sh -p news/crawler/github/github_notification_crawler.py
```

## 常见问题

### Q: 代理认证失败（407 错误）
**A**: 检查代理 URL 格式是否正确，确保使用 `http://` 协议

### Q: MongoDB 连接失败（Connection refused）
**A**: 确保 MongoDB 服务已启动，端口 27017 未被占用

### Q: GitHub API 返回 401 错误
**A**: 检查 `GITHUB_TOKEN` 是否有效，是否有足够的权限

### Q: TLS in TLS 错误
**A**: 将代理 URL 从 `https://` 改为 `http://`

## 下一步

配置完成后，运行完整的爬虫流程：

```bash
# 运行所有爬虫
./script/run.sh

# 或运行特定类别的爬虫
./script/run.sh -p news/crawler/tech_news/tech_news_crawler.py
```
