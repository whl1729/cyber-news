## Context

The project has an established pattern for AI blog crawlers in `news/crawler/ai/`. Each crawler follows the same structure: a `WebParser` subclass that parses HTML and returns a list of dicts, and a `crawl()` function that uses `web_crawler.crawl()`. Reporters are thin wrappers around `DailyNewsReporter`.

Three new sources need to be added:
1. **Cursor Blog** (`cursor.com/blog`) — a Next.js SSR page that renders blog article links with dates in anchor text
2. **Martin Fowler's "Exploring Gen AI" series** (`martinfowler.com/articles/exploring-gen-ai.html`) — a static HTML index page listing each article as `<p class="memo"><a href="...">Title</a><span class="date"> (DD Month YYYY)</span></p>`
3. **Lance Martin's Blog** (`rlancemartin.github.io`) — a Jekyll-style GitHub Pages site with `<ul class="post-list">` containing `<span class="post-meta">` dates and `<a class="post-link">` links

## Goals / Non-Goals

**Goals:**
- Add three crawlers following the existing `WebParser` + `crawl()` pattern
- Register crawlers in `ai_crawler.py` and reporters in `news_reporter.py`
- Add to `config/cyber_news_config.yaml` so they run by default

**Non-Goals:**
- Full-text crawling of individual articles
- Selenium/JS rendering (all three pages render HTML server-side)
- Pagination beyond the default landing page

## Decisions

**D1: Cursor Blog — scrape cursor.com/blog (English) instead of cursor.com/cn/blog**
The canonical URL is `cursor.com/blog`; `/cn/blog` is a localized mirror. Article URLs are at `/blog/<slug>`. Using the canonical ensures consistent `id` values (the slug or title).
Alternative: use `/cn/blog` — rejected because it's a localized mirror and IDs would differ.

**D2: Martin Fowler — crawl the series index page, not individual articles**
The index page `articles/exploring-gen-ai.html` lists all episodes with titles, dates, and relative URLs in a structured `<p class="memo">` pattern. This is simpler and more reliable than crawling the site's atom feed or individual article pages.
Alternative: Use the site's Atom feed — rejected because the feed aggregates all content from martinfowler.com, not just this series.

**D3: Date formats**
- Cursor: dates appear inline in anchor text like `"Mar 19, 2026·Research..."` — parse the leading date segment
- Martin Fowler: dates appear as `(DD Month YYYY)` in a `<span class="date">` — straightforward `strptime`
- Lance Martin: dates appear as `Jan 9, 2026` in `<span class="post-meta">` — straightforward `strptime`

**D4: No reporter files needed — use inline DailyNewsReporter in news_reporter.py**
The existing pattern since the DeepMind/HuggingFace refactor is to instantiate `DailyNewsReporter` directly in `news_reporter.py` rather than creating a separate reporter module per source. Follow this pattern.

## Risks / Trade-offs

- **Cursor blog is a Next.js app** — the HTML is server-rendered so `curl` returns full content, but if Cursor moves to full client-side rendering this will break. → Mitigation: if parsing returns 0 results, fall back to Selenium or RSS.
- **Martin Fowler date parsing** — date format `(DD Month YYYY)` includes parentheses and spaces; must strip carefully. → Mitigation: use regex or `strip('() ')` before `strptime`.
- **Lance Martin blog has few posts** — the blog is low-frequency. On repeated runs, `insert_many_new()` will deduplicate. No action needed.
