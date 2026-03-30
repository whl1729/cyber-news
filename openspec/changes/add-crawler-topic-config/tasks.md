## 1. Configuration Setup

- [x] 1.1 Add `enabled_topics` list to `config/cyber_news_config.yaml` with example topic names
- [x] 1.2 Update `news/util/configer.py` to expose `get_enabled_topics()` method that returns the list (or None if not configured)

## 2. Blog Crawler Filtering

- [x] 2.1 Modify `news/crawler/blog/blog_crawler.py` to check if `ruanyifeng_weekly` is enabled before calling its crawler

## 3. GitHub Crawler Filtering

- [x] 3.1 Modify `news/crawler/github/github_crawler.py` to check if `github_received_event` is enabled
- [x] 3.2 Add check for `github_notification` topic
- [x] 3.3 Add check for `github_trending` topic

## 4. Language Crawler Filtering

- [x] 4.1 Modify `news/crawler/language/language_crawler.py` to check if `cpp_blog` is enabled
- [x] 4.2 Add check for `go_blog` topic
- [x] 4.3 Add check for `python_blog` topic
- [x] 4.4 Add check for `rust_blog` topic

## 5. Tech News Crawler Filtering

- [x] 5.1 Modify `news/crawler/tech_news/tech_news_crawler.py` to check if `hacker_news` is enabled
- [x] 5.2 Add check for `jiqizhixin` topic
- [x] 5.3 Add check for `liangziwei` topic
- [x] 5.4 Add check for `xinzhiyuan` topic

## 6. Testing and Validation

- [x] 6.1 Test with empty/missing `enabled_topics` config (should enable all crawlers)
- [x] 6.2 Test with partial topic list (should skip disabled topics and log appropriately)
