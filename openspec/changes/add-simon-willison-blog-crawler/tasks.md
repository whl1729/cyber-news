## 1. Crawler Implementation

- [x] 1.1 Create simon_willison_blog_crawler.py file in news/crawler/ai/
- [x] 1.2 Implement SimonWillisonBlogParser class inheriting from WebParser
- [x] 1.3 Implement parse() method to extract blog posts from HTML
- [x] 1.4 Implement _parse_item() method to extract title, URL, and date from each post
- [x] 1.5 Implement custom date parsing for "30th March 2026" format with ordinal suffixes
- [x] 1.6 Handle relative URLs by prepending https://simonwillison.net
- [x] 1.7 Implement crawl() function using web_crawler.crawl() utility
- [x] 1.8 Add module-level constants for URL, base URL, and collection name

## 2. Crawler Registration

- [x] 2.1 Register simon_willison_blog crawler in ai_crawler.py crawlers dict
- [x] 2.2 Add get_enabled_topics() check to allow configuration-based enable/disable
- [x] 2.3 Add appropriate logging messages for enabled/disabled crawler

## 3. Reporter Integration

- [x] 3.1 Add DailyNewsReporter for Simon Willison Blog to news_reporter.py
- [x] 3.2 Set order_by="created_at" to sort by publication date
- [x] 3.3 Position reporter appropriately in daily_reporters list (after Sebastian Raschka Blog)

## 4. Configuration

- [x] 4.1 Add "simon_willison_blog" to enabled_topics in config/cyber_news_config.yaml

## 5. Testing and Validation

- [x] 5.1 Run crawler with offline HTML file to verify parsing works correctly
- [x] 5.2 Verify data is inserted into simon_willison_blog collection in MongoDB
- [x] 5.3 Run daily news reporter to verify Simon Willison Blog section appears in report
- [x] 5.4 Verify blog posts are ordered by created_at in descending order
- [x] 5.5 Run pre-commit hooks to ensure code formatting and linting
- [x] 5.6 Run full integration test: ./script/run.sh -l debug
