## Context

HuggingFace (https://huggingface.co/blog) is a leading AI platform publishing blog posts on model releases, research, and open-source tools. This follows the established pattern of crawling AI organization blogs (DeepMind, OpenAI, etc.).

**Current state**: No HuggingFace blog crawler exists.

**Constraints**:
- Network access to huggingface.co may require proxy or Selenium (JS-rendered content)
- Must follow existing crawler patterns (WebCrawler + WebParser)
- Must integrate with MongoDB storage and daily reporter

## Goals / Non-Goals

**Goals:**
- Crawl blog post metadata (title, URL, publication date) from huggingface.co/blog
- Store in MongoDB collection `huggingface_blog`
- Generate daily report section sorted by publication date descending
- Support topic-based filtering via `enabled_topics`

**Non-Goals:**
- Crawling full article content (only metadata)
- Historical backfill beyond what's visible on the main blog page
- Multi-page pagination (initial implementation crawls first page only)

## Decisions

### Use Selenium for rendering
**Decision**: Use `use_selenium=True` in web_crawler.crawl() call

**Rationale**: HuggingFace blog likely uses JavaScript rendering (common for modern React/Next.js sites). Selenium ensures we get fully rendered HTML.

**Alternative considered**: Plain HTTP requests - simpler but may return empty/incomplete HTML if JS-rendered.

### Date parsing strategy
**Decision**: Parse date format after inspecting actual HTML. Common formats: ISO 8601, "Month DD, YYYY", or relative dates ("2 days ago").

**Fallback**: If date parsing fails, use current date as `created_at` (consistent with other crawlers).

### Deduplication key
**Decision**: Use post title as `id` field (display name), deduplicate by `id` in MongoDB

**Rationale**: Consistent with existing blog crawlers (Yohei, DeepMind). Assumes titles are unique.

## Risks / Trade-offs

**[Risk]** HuggingFace may block automated requests or require authentication
→ **Mitigation**: Use proxy via `config["proxies"]` and Selenium with browser user agent

**[Risk]** HTML structure may change, breaking the parser
→ **Mitigation**: Add robust error handling and logging. Monitor crawler health via logs.

**[Risk]** Date format may vary or be missing
→ **Mitigation**: Fallback to current date if parsing fails (logged as warning)

**[Trade-off]** Selenium is slower than plain HTTP
→ **Accepted**: Reliability over speed for blog crawling (not time-critical)
