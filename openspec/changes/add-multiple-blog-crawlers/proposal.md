## Why

The project currently tracks a curated set of AI/tech blogs. Adding 18 more influential blogs from engineers, researchers, and thought leaders will provide broader coverage of the tech ecosystem.

## What Changes

- Add 18 new blog crawlers in `news/crawler/ai/`
- Add 18 new reporters or register them via `DailyNewsReporter` in `news/reporter/news_reporter.py`
- Register all 18 topics in `config/cyber_news_config.yaml`

Blogs to add:
- BaoYu Blog (https://baoyu.io/)
- Sam Altman Blog (https://blog.samaltman.com/)
- Mario Zechner (https://mariozechner.at)
- David Heinemeier Hansson (https://world.hey.com/dhh)
- Armin Ronacher (https://lucumr.pocoo.org)
- antirez (https://antirez.com/latest/0)
- Ryan Dahl (https://tinyclouds.org)
- The Pragmatic Engineer (https://newsletter.pragmaticengineer.com)
- sean goedecke (https://www.seangoedecke.com)
- Philipp Schmid (https://www.philschmid.de)
- Matt Shumer (https://shumer.dev/blog)
- Bassim Eledath (https://www.bassimeledath.com/blog)
- Rob Zolkos (https://www.zolkos.com/)
- Chris Gregori (https://www.chrisgregori.dev/)
- Addy Osmani (https://addyosmani.com/blog/)
- Uwe Friedrichsen (https://www.ufried.com/)
- One Useful Thing (https://www.oneusefulthing.org)
- Han, Not Solo (https://leehanchung.github.io/blogs/)

## Capabilities

### New Capabilities

- `baoyu-blog`: Crawl BaoYu's blog posts (title, URL, date)
- `sam-altman-blog`: Crawl Sam Altman's blog posts
- `mario-zechner-blog`: Crawl Mario Zechner's blog posts
- `dhh-blog`: Crawl David Heinemeier Hansson's blog posts
- `armin-ronacher-blog`: Crawl Armin Ronacher's blog posts
- `antirez-blog`: Crawl antirez's blog posts
- `ryan-dahl-blog`: Crawl Ryan Dahl's blog posts
- `pragmatic-engineer-blog`: Crawl The Pragmatic Engineer newsletter posts
- `sean-goedecke-blog`: Crawl Sean Goedecke's blog posts
- `philipp-schmid-blog`: Crawl Philipp Schmid's blog posts
- `matt-shumer-blog`: Crawl Matt Shumer's blog posts
- `bassim-eledath-blog`: Crawl Bassim Eledath's blog posts
- `rob-zolkos-blog`: Crawl Rob Zolkos's blog posts
- `chris-gregori-blog`: Crawl Chris Gregori's blog posts
- `addy-osmani-blog`: Crawl Addy Osmani's blog posts
- `uwe-friedrichsen-blog`: Crawl Uwe Friedrichsen's blog posts
- `one-useful-thing-blog`: Crawl One Useful Thing newsletter posts
- `han-not-solo-blog`: Crawl Han, Not Solo blog posts

### Modified Capabilities

(none)

## Impact

- 18 new crawler files in `news/crawler/ai/`
- `news/crawler/ai/ai_crawler.py`: register 18 new crawlers
- `news/reporter/news_reporter.py`: add 18 entries to `daily_reporters`
- `config/cyber_news_config.yaml`: add 18 new topics to `enabled_topics`
