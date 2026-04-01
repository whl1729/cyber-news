## 1. Crawler Implementation

- [x] 1.1 Create `news/crawler/ai/chip_huyen_blog_crawler.py` with `ChipHuyenBlogParser` and `crawl()` function
- [x] 1.2 Register `chip_huyen_blog_crawler` in `news/crawler/ai/ai_crawler.py` under topic key `"chip_huyen_blog"`

## 2. Reporter Integration

- [x] 2.1 Add `DailyNewsReporter("Chip Huyen Blog", "chip_huyen_blog", order_by="created_at")` to `news/reporter/news_reporter.py`

## 3. Config

- [x] 3.1 Add `chip_huyen_blog` to `enabled_topics` in `config/cyber_news_config.yaml`

## 4. Verification

- [x] 4.1 Run crawler and verify posts are inserted: `./script/run.sh -p news/crawler/ai/chip_huyen_blog_crawler.py -l debug`
- [x] 4.2 Run reporter and verify "Chip Huyen Blog" section appears sorted by date: `./script/run.sh -p news/reporter/news_reporter.py -l debug`
- [x] 4.3 Run pre-commit checks on modified files
