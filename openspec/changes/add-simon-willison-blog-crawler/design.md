## Context

The Cyber News project aggregates technical news from various sources using a crawler-based architecture. Currently, the AI crawler section includes blogs from Chip Huyen, Claude Code Blog, Karpathy Blog, Sebastian Raschka Blog, and OpenAI News. Simon Willison's Weblog is a valuable source for AI, SQLite, Python, and programming-related content that should be added.

Existing pattern:
- Crawlers inherit from `WebParser` base class and implement `parse()` method
- Blog crawlers parse HTML to extract title, URL, date, and description
- Data stored in MongoDB with `crawled_at` timestamp
- Reporters use `DailyNewsReporter` with `order_by="created_at"` for blog posts

The blog HTML structure uses entries wrapped in `<div class="entry segment" data-type="entry">` elements containing title links in `<h3>` tags and dates in `<div class="entryFooter">` with format like "2:28 pm / 30th March 2026".

## Goals / Non-Goals

**Goals:**
- Create a crawler for Simon Willison's Weblog (simonwillison.net/entries/)
- Extract blog post titles, URLs, and publication dates
- Store data in MongoDB collection `simon_willison_blog`
- Add blog posts to daily news reports in reverse chronological order
- Follow existing patterns for consistency

**Non-Goals:**
- Implementing caching mechanisms (handled by web_crawler utility)
- Handling authentication (blog is public)
- Implementing retry logic (handled by web_crawler utility)
- Extracting tags or descriptions (not required for current use case)

## Decisions

**1. Use existing WebParser pattern**
- **Decision**: Create `SimonWillisonBlogParser` class inheriting from `WebParser`
- **Rationale**: Consistent with existing blog crawlers (Chip Huyen, Karpathy, Sebastian Raschka, Claude Code). Leverages existing infrastructure for web fetching, MongoDB insertion, and logging.
- **Alternative**: Create standalone crawler without inheritance. Rejected because it would require duplicating existing functionality.

**2. Date format handling**
- **Decision**: Use custom date parsing for Simon Willison's unique format
- **Rationale**: Simon Willison's blog uses format like "30th March 2026" or "27th March 2026" with ordinal suffixes (st, nd, rd, th). Existing timelib functions may not handle this format, so custom parsing is needed.
- **Alternative**: Use existing timelib.format_date_6(). Rejected because it expects "Mar 30, 2026" format without ordinal suffixes.

**3. Collection naming**
- **Decision**: Use `simon_willison_blog` as MongoDB collection name
- **Rationale**: Follows existing naming convention (e.g., `chip_huyen_blog`, `sebastian_raschka_blog`). Descriptive and consistent with codebase patterns.

**4. Registration in AI crawler**
- **Decision**: Register in `ai_crawler.py` using dict pattern with `get_enabled_topics()`
- **Rationale**: Allows enabling/disabling via configuration. Follows established pattern for crawler management.

**5. DailyNewsReporter configuration**
- **Decision**: Use `order_by="created_at"` to sort by publication date
- **Rationale**: Blog posts should appear in reverse chronological order. Same pattern as other blog reporters (Chip Huyen, Karpathy, Sebastian Raschka, Claude Code).

**6. URL handling**
- **Decision**: All URLs are relative paths starting with `/YYYY/Month/Day/slug/`
- **Rationale**: Simon Willison's blog consistently uses relative URLs. Prepending base URL `https://simonwillison.net` will create absolute URLs.

## Risks / Trade-offs

**Risk**: Blog HTML structure may change
- **Mitigation**: Use flexible BeautifulSoup selectors (class-based), not brittle position-based parsing

**Risk**: Date format variations may cause parsing failures
- **Mitigation**: Implement robust date parsing that handles various ordinal suffixes (st, nd, rd, th) and month abbreviations. Add error handling in `_parse_item()` method to skip malformed entries.

**Risk**: Description text is optional in Simon Willison's blog entries
- **Acceptance**: Some posts may have excerpt text in `<p>` tags, others may not. This is acceptable as the title and URL are always present.

**Trade-off**: Not extracting tags from posts
- **Acceptance**: Simon Willison's posts have rich tagging (AI, LLM, Python, etc.), but extracting tags is not required for the current scope. Can be added later if needed.
