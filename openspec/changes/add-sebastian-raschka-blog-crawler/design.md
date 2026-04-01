## Context

The Cyber News project aggregates technical news from various sources using a crawler-based architecture. Currently, the AI crawler section includes blogs from Chip Huyen, Claude Code Blog, Karpathy Blog, and OpenAI News. Sebastian Raschka's blog is a valuable AI/LLM research source that should be added.

Existing pattern:
- Crawlers inherit from `WebParser` base class and implement `parse()` method
- Blog crawlers parse HTML to extract title, URL, date, and description
- Data stored in MongoDB with `crawled_at` timestamp
- Reporters use `DailyNewsReporter` with `order_by="created_at"` for blog posts

The blog HTML structure uses Jekyll with blog posts wrapped in `<div class="post-entry">` elements containing title links and post dates.

## Goals / Non-Goals

**Goals:**
- Create a crawler for Sebastian Raschka's blog (sebastianraschka.com)
- Extract blog post titles, URLs, publication dates, and descriptions
- Store data in MongoDB collection `sebastian_raschka_blog`
- Add blog posts to daily news reports in reverse chronological order
- Follow existing patterns for consistency

**Non-Goals:**
- Implementing caching mechanisms (handled by web_crawler utility)
- Handling authentication (blog is public)
- Implementing retry logic (handled by web_crawler utility)

## Decisions

**1. Use existing WebParser pattern**
- **Decision**: Create `SebastianRaschkaBlogParser` class inheriting from `WebParser`
- **Rationale**: Consistent with existing blog crawlers (Chip Huyen, Karpathy, Claude Code). Leverages existing infrastructure for web fetching, MongoDB insertion, and logging.
- **Alternative**: Create standalone crawler without inheritance. Rejected because it would require duplicating existing functionality.

**2. Date format handling**
- **Decision**: Use `timelib.format_date_6()` for date parsing
- **Rationale**: Sebastian Raschka's blog uses "Month Day, Year" format (e.g., "Mar 22, 2026"). The `timelib` module already handles this format.
- **Alternative**: Create custom date parser. Rejected to avoid code duplication.

**3. Collection naming**
- **Decision**: Use `sebastian_raschka_blog` as MongoDB collection name
- **Rationale**: Follows existing naming convention (e.g., `chip_huyen_blog`, `karpathy_blog`). Descriptive and consistent with codebase patterns.

**4. Registration in AI crawler**
- **Decision**: Register in `ai_crawler.py` using dict pattern with `get_enabled_topics()`
- **Rationale**: Allows enabling/disabling via configuration. Follows established pattern for crawler management.

**5. DailyNewsReporter configuration**
- **Decision**: Use `order_by="created_at"` to sort by publication date
- **Rationale**: Blog posts should appear in reverse chronological order. Same pattern as other blog reporters (Chip Huyen, Karpathy, Claude Code).

## Risks / Trade-offs

**Risk**: Blog HTML structure may change
- **Mitigation**: Use flexible BeautifulSoup selectors (class-based), not brittle position-based parsing

**Risk**: Date format variations may cause parsing failures
- **Mitigation**: The `timelib.format_date_6()` function handles multiple date formats. Add error handling in `_parse_item()` method to skip malformed entries

**Risk**: External links to magazine.sebastianraschka.com vs internal links
- **Mitigation**: Handle both absolute URLs (starting with https://) and relative URLs (starting with /) by checking href prefix

**Trade-off**: Description text is optional in Sebastian Raschka's blog entries
- **Acceptance**: Some posts may have empty descriptions. This is acceptable as the title and URL are always present.
