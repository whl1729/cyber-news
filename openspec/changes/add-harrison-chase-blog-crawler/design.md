## Context

The Cyber News project aggregates technical news from various sources using a crawler-based architecture. Currently, the AI crawler section includes blogs from Chip Huyen, Claude Code Blog, Karpathy Blog, Sebastian Raschka Blog, Simon Willison Blog, and OpenAI News. Harrison Chase's blog on LangChain is a valuable source for AI/LLM, agent-based systems, and practical AI implementation that should be added.

Existing pattern:
- Crawlers inherit from `WebParser` base class and implement `parse()` method
- Blog crawlers parse HTML to extract title, URL, date, and description
- Data stored in MongoDB with `crawled_at` timestamp
- Reporters use `DailyNewsReporter` with `order_by="created_at"` for blog posts

The blog HTML structure uses articles wrapped in `<article class="post-card">` elements containing title links in `<h2>` tags. Date information appears to be in image filenames (e.g., `Screenshot-2026-02-09-at-9.30.02---PM.png`) but this is not reliable for publication date.

## Goals / Non-Goals

**Goals:**
- Create a crawler for Harrison Chase's blog (blog.langchain.com/author/harrison/)
- Extract blog post titles, URLs, and publication dates
- Store data in MongoDB collection `harrison_chase_blog`
- Add blog posts to daily news reports in reverse chronological order
- Follow existing patterns for consistency

**Non-Goals:**
- Implementing caching mechanisms (handled by web_crawler utility)
- Handling authentication (blog is public)
- Implementing retry logic (handled by web_crawler utility)
- Extracting tags or descriptions (not required for current use case)

## Decisions

**1. Use existing WebParser pattern**
- **Decision**: Create `HarrisonChaseBlogParser` class inheriting from `WebParser`
- **Rationale**: Consistent with existing blog crawlers (Chip Huyen, Karpathy, Sebastian Raschka, Simon Willison). Leverages existing infrastructure for web fetching, MongoDB insertion, and logging.
- **Alternative**: Create standalone crawler without inheritance. Rejected because it would require duplicating existing functionality.

**2. Date format handling**
- **Decision**: Extract date from image filename pattern as fallback, but prioritize more reliable sources
- **Rationale**: The blog shows relative reading time ("X min read") in HTML, not publication date. Image filenames contain datetime like `Screenshot-2026-02-09-at-9.30.02---PM.png`. We can parse this pattern to get approximate publication date.
- **Alternative**: Try to find JSON API or RSS feed. Rejected because it requires additional investigation and may not always be available.
- **Fallback**: If date parsing fails, use crawled_at as date for ordering.

**3. Collection naming**
- **Decision**: Use `harrison_chase_blog` as MongoDB collection name
- **Rationale**: Follows existing naming convention (e.g., `chip_huyen_blog`, `simon_willison_blog`). Descriptive and consistent with codebase patterns.

**4. Registration in AI crawler**
- **Decision**: Register in `ai_crawler.py` using dict pattern with `get_enabled_topics()`
- **Rationale**: Allows enabling/disabling via configuration. Follows established pattern for crawler management.

**5. DailyNewsReporter configuration**
- **Decision**: Use `order_by="created_at"` to sort by publication date
- **Rationale**: Blog posts should appear in reverse chronological order. Same pattern as other blog reporters (Chip Huyen, Karpathy, Sebastian Raschka, Simon Willison, Claude Code).

**6. URL handling**
- **Decision**: All URLs are relative paths starting with `/` or absolute
- **Rationale**: Harrison Chase's blog uses a mix of relative paths and potentially absolute URLs. Prepending base URL `https://blog.langchain.com` when needed will create absolute URLs.

## Risks / Trade-offs

**Risk**: Blog HTML structure may change
- **Mitigation**: Use flexible BeautifulSoup selectors (class-based), not brittle position-based parsing

**Risk**: Date extraction from image filenames is approximate, not exact
- **Mitigation**: Use regex to parse datetime from filename pattern `Screenshot-YYYY-MM-DD-at-HH.MM.SS---AM/PM.png`. This gives close approximation of publication date. Add fallback to crawled_at if parsing fails.

**Risk**: Some posts may not have images with date information
- **Acceptance**: Some posts may rely on crawled_at timestamp for ordering. This is acceptable as long as posts are consistently ordered within batch.

**Trade-off**: Not extracting tags or descriptions
- **Acceptance**: Harrison Chase's posts have rich tagging (AI, LLM, agents, etc.), but extracting tags is not required for current scope. Can be added later if needed.
