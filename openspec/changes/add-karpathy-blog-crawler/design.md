## Context

The project already has an `ai_crawler.py` that orchestrates AI-related crawlers using the `dict` + `get_enabled_topics()` pattern. The existing `claude_code_blog_crawler.py` and `openai_news_crawler.py` serve as reference implementations. Karpathy's blog is a simple Jekyll static site—no JavaScript rendering, no bot protection—so a plain `requests.get()` with proxy is sufficient.

## Goals / Non-Goals

**Goals:**
- Add a crawler for `https://karpathy.github.io` that extracts post title, URL, date, and description
- Store posts in MongoDB collection `karpathy_blog`
- Register the crawler in `ai_crawler.py` using the standard topic-dict pattern
- Display Karpathy blog posts in the daily news report, ordered by `created_at` descending

**Non-Goals:**
- Crawling individual post content (only the index page)
- Pagination (the index page lists all posts)
- Incremental/delta crawling (existing `insert_many_new` handles deduplication)

## Decisions

### Use `myrequests.get()` with proxy
The site is a plain static HTML site (GitHub Pages / Jekyll). No TLS fingerprinting or JavaScript rendering required. Use `myrequests.get()` with `proxies=config["proxies"]` for consistency with other crawlers that need proxy access.

Alternative: No proxy. Rejected because the machine's network may be restricted; using proxy is safe and consistent.

### Parse date from `<span class="post-date">`
The date is rendered as "Feb 12, 2026". Use Python's `datetime.strptime` with format `"%b %d, %Y"` and convert to ISO `YYYY-MM-DD` string for `created_at`.

### Use `href` to construct canonical URL
Post URLs are relative (`/2026/02/12/microgpt/`). Prepend `https://karpathy.github.io` to form the absolute URL. The `id` field will be the relative href to ensure uniqueness.

## Risks / Trade-offs

- [Date format change] → Karpathy could change the blog's date format. Mitigation: wrap date parsing in try/except and log a warning on failure.
- [Site unavailability] → GitHub Pages is generally reliable. Mitigation: `myrequests.get()` already retries on failure.
