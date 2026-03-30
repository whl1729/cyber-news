## Context

The Cyber News crawler currently executes all crawlers unconditionally. Users need selective control over which news topics are crawled to optimize resource usage and focus on relevant sources.

The current architecture has a hierarchical crawler structure:
- `news_crawler.py` calls category crawlers (blog, github, language, tech_news)
- Each category crawler calls individual topic crawlers
- No configuration mechanism exists to skip specific crawlers

## Goals / Non-Goals

**Goals:**
- Add YAML-based configuration to enable/disable individual crawler topics
- Maintain backward compatibility (all topics enabled by default if not configured)
- Minimal code changes to existing crawler structure

**Non-Goals:**
- Dynamic runtime topic toggling (configuration read at startup only)
- Topic dependency management (topics are independent)
- Per-user topic preferences (single global configuration)

## Decisions

### Decision 1: Configuration structure
Use a flat list of enabled topic names in `cyber_news_config.yaml`:
```yaml
enabled_topics:
  - ruanyifeng_weekly
  - github_trending
  - hacker_news
```

**Rationale**: Simple and explicit. Alternative hierarchical structure (grouping by category) adds complexity without clear benefit.

### Decision 2: Topic naming convention
Use snake_case names matching the crawler module names (e.g., `ruanyifeng_weekly`, `github_trending`).

**Rationale**: Consistent with Python module naming. Makes it easy to map configuration to code.

### Decision 3: Filtering location
Implement filtering in category crawler files (blog_crawler.py, github_crawler.py, etc.) rather than in individual crawlers.

**Rationale**: Centralized control per category. Individual crawlers remain unaware of filtering logic, maintaining separation of concerns.

### Decision 4: Default behavior
If `enabled_topics` is not present in config, enable all topics.

**Rationale**: Backward compatibility. Existing deployments continue working without configuration changes.

## Risks / Trade-offs

**Risk**: Topic name typos in configuration silently disable crawlers
→ **Mitigation**: Log warning for unrecognized topic names at startup

**Trade-off**: Flat list requires updating config when adding new crawlers
→ **Acceptable**: New crawlers are infrequent, explicit configuration is clearer than wildcards
