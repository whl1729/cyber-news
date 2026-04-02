## Context

The project already has a pattern for blog crawlers under `news/crawler/ai/`. Each crawler follows the same `WebParser` → `web_crawler.crawl()` pattern. The `ai_crawler.py` aggregates them via a dict and `get_enabled_topics()`. Reporters are `DailyNewsReporter` instances registered in `news_reporter.py`.

Each new blog needs: HTML structure inspection, a parser class, a `crawl()` function, registration in `ai_crawler.py`, a reporter entry in `news_reporter.py`, and a topic entry in `config/cyber_news_config.yaml`.

## Goals / Non-Goals

**Goals:**
- Add crawlers for all 18 blogs
- Each crawler extracts title, URL, and publication date
- Each topic registered and toggleable via `enabled_topics` config
- Reporters output posts sorted by `created_at` descending

**Non-Goals:**
- Full article content extraction
- Comment/discussion scraping
- Subpage following

## Decisions

**One crawler file per blog**: Consistent with existing pattern (`karpathy_blog_crawler.py`, `chip_huyen_blog_crawler.py`, etc.). Keeps each crawler isolated and easy to debug.

**RSS-first approach for date accuracy**: Many blogs expose RSS/Atom feeds which provide structured dates. Where available, parse the RSS feed (`<pubDate>` or `<published>`) instead of scraping HTML. This is more reliable and less brittle than HTML parsing.

**HTML scraping fallback**: Where no RSS feed exists or feed is paywalled (e.g., Pragmatic Engineer), scrape HTML. Use `curl_cffi` via `web_crawler.crawl()` with `use_selenium=False` and proxy where needed.

**Collection naming**: Use snake_case matching the blog name (e.g., `baoyu_blog`, `sam_altman_blog`, `dhh_blog`, `armin_ronacher_blog`, `antirez_blog`, `ryan_dahl_blog`, `pragmatic_engineer_blog`, `sean_goedecke_blog`, `philipp_schmid_blog`, `matt_shumer_blog`, `bassim_eledath_blog`, `rob_zolkos_blog`, `chris_gregori_blog`, `addy_osmani_blog`, `uwe_friedrichsen_blog`, `one_useful_thing_blog`, `han_not_solo_blog`).

**Date format**: Store as `YYYY-MM-DD` string in `created_at`. Parse from RSS `pubDate` (RFC 2822) or ISO 8601 as appropriate. Fall back to `datetime.now().strftime("%Y-%m-%d")` if parsing fails.

**`id` field**: Use post title as `id` (consistent with other crawlers). MongoDB's `insert_many_new()` deduplicates on `id`.

## Risks / Trade-offs

- **Site structure changes** → Brittle HTML parsers. Mitigation: log warnings, fall back gracefully, prefer RSS.
- **Paywalled content** (Pragmatic Engineer) → May only see preview/teaser. Mitigation: crawl what's publicly available (post list page).
- **Low-traffic blogs** → Some blogs may have very few recent posts. Mitigation: still crawl, report will just show fewer items.
- **proxy requirement** → Some sites may be blocked without proxy. Mitigation: pass `proxies=config["proxies"]` consistently.

## Migration Plan

1. Inspect each blog URL to determine HTML structure or RSS availability
2. Implement each crawler, test individually
3. Register in `ai_crawler.py`, `news_reporter.py`, `config/cyber_news_config.yaml`
4. Run full verification per CLAUDE.md mandatory steps
