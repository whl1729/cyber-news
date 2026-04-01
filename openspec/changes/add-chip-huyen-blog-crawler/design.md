## Context

The project already has a pattern for AI blog crawlers (Karpathy Blog, Claude Code Blog, OpenAI News) all under `news/crawler/ai/`. Chip Huyen's blog (`https://huyenchip.com/blog/`) is a Jekyll-generated static site with a simple `<ul class="post-list">` structure — similar to Karpathy's `<ul class="posts">`. The page uses Cloudflare (`cf-2fa-verify` meta tag present in the HTML), but the blog listing page is served as static HTML and is publicly accessible without JS-rendered content.

## Goals / Non-Goals

**Goals:**
- Crawl `https://huyenchip.com/blog/` and store post title, URL, and publish date in MongoDB collection `chip_huyen_blog`
- Report posts in `news_reporter.py` sorted by `created_at` descending (consistent with other blog sources)
- Support enable/disable via `enabled_topics` config

**Non-Goals:**
- Crawling full post body content
- Handling pagination (the blog lists all posts on a single page)
- JS rendering / Selenium (the blog listing is static HTML)

## Decisions

**Use `web_crawler.crawl()` (not `curl_cffi`)**: The `huyenchip.com/blog/` listing page is plain static HTML served by Cloudflare, similar to `karpathy.github.io`. While Cloudflare is present, a `requests`-based crawl with proxy should succeed since there's no bot challenge on the listing page (confirmed by manual download of the HTML). If this fails in production, fall back to `curl_cffi` like `openai_news_crawler`.

**Use `timelib.format_date_6()`**: Dates appear as "Jan 16, 2025" (abbreviated month + day + year), which matches the `%b %d, %Y` format already handled by `format_date_6`.

**Set `id = title`**: Consistent with all other crawlers in this project — `DailyNewsReporter._get_news()` uses `news['id']` as the displayed link text, so `id` must be the human-readable title.

## Risks / Trade-offs

- [Cloudflare blocking] → Mitigation: Use proxy (`config["proxies"]`); if blocked, switch to `curl_cffi` impersonation
- [HTML structure changes] → Mitigation: Log warning and return empty list if `post-list` ul not found

## Migration Plan

No migration needed — new MongoDB collection `chip_huyen_blog` is created automatically on first insert.
