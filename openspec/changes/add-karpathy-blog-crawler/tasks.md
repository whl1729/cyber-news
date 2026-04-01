## 1. Crawler Implementation

- [x] 1.1 Create `news/crawler/ai/karpathy_blog_crawler.py` with `KarpathyBlogParser` and `crawl()` function
- [x] 1.2 Register `karpathy_blog_crawler` in `news/crawler/ai/ai_crawler.py` under topic key `"karpathy_blog"`

## 2. Reporter Integration

- [x] 2.1 Add `DailyNewsReporter("Karpathy Blog", "karpathy_blog", order_by="created_at")` to `news/reporter/news_reporter.py`

## 3. Verification

- [x] 3.1 Run crawler and verify posts are inserted: `./script/run.sh -p news/crawler/ai/karpathy_blog_crawler.py -l debug`
- [x] 3.2 Run reporter and verify "Karpathy Blog" section appears sorted by date: `./script/run.sh -p news/reporter/news_reporter.py -l debug`
- [x] 3.3 Run pre-commit checks on modified files
