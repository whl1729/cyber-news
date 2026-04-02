## Context

The cyber-news project currently crawls multiple AI-related blogs (Claude Code, OpenAI, Karpathy, Chip Huyen, Sebastian Raschka, Simon Willison, Harrison Chase). Yohei Nakajima is a prominent figure in the AI agent space, known for creating BabyAGI. Adding his blog follows the established pattern of crawling influential AI researchers' blogs.

The existing codebase has:
- A consistent pattern for blog crawlers in `news/crawler/ai/`
- A `WebCrawler` utility class for HTTP requests and MongoDB operations
- A `DailyNewsReporter` base class for generating report sections
- Registration mechanisms in `ai_crawler.py` and `news_reporter.py`

## Goals / Non-Goals

**Goals:**
- Add Yohei Nakajima's blog as a new data source following existing patterns
- Ensure blog posts are sorted by publication date (newest first) in reports
- Maintain consistency with other blog crawlers in the codebase

**Non-Goals:**
- Scraping full blog post content (only metadata: title, URL, date)
- Real-time updates or webhooks (follows existing batch crawl pattern)
- Custom parsing logic beyond what's needed for this specific blog structure

## Decisions

### Decision 1: Follow existing blog crawler pattern
**Rationale:** The codebase has 7 existing blog crawlers with a proven pattern. Consistency reduces maintenance burden and makes the code predictable.

**Implementation approach:**
- Use `WebCrawler` class from `news.util.web_crawler`
- Implement a `crawl()` function as entry point
- Parse HTML using BeautifulSoup (standard in this codebase)
- Store in MongoDB collection `yohei_nakajima_blog`

**Alternatives considered:**
- Custom crawler implementation: Rejected due to unnecessary complexity
- RSS feed parsing: Blog may not have RSS, HTML parsing is more reliable

### Decision 2: Use created_at for sorting in reporter
**Rationale:** Per CLAUDE.md guidelines, blog sources with explicit publication dates must use `order_by="created_at"` to ensure chronological ordering in reports.

**Implementation:**
- Reporter inherits from `DailyNewsReporter`
- Specify `order_by="created_at"` parameter
- Extract publication date during crawling and store as `created_at` field

**Alternatives considered:**
- Default `crawled_at` sorting: Incorrect for blogs with publication dates
- Manual sorting in reporter: Unnecessary when base class supports it

### Decision 3: Register in ai_crawler.py dict structure
**Rationale:** Per CLAUDE.md, all crawlers must use dict structure with `get_enabled_topics()` for configuration-based enabling/disabling.

**Implementation:**
- Add `"yohei_nakajima_blog": yohei_nakajima_blog_crawler` to crawlers dict
- Topic name matches MongoDB collection name convention
- Controlled via `enabled_topics` in config file

## Risks / Trade-offs

**Risk:** Blog HTML structure changes → Mitigation: Follow existing error handling patterns, log parsing failures gracefully

**Risk:** Blog may not have machine-readable publication dates → Mitigation: Inspect blog structure first, fall back to crawled_at if needed

**Trade-off:** No full-text indexing → Acceptable, consistent with other blog crawlers that only store metadata
