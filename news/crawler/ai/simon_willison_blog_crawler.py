from datetime import datetime
from typing import List

from bs4 import BeautifulSoup

from news.util import web_crawler
from news.util.configer import config
from news.util.logger import logger
from news.util.web_parser import WebParser

SIMON_WILLISON_BLOG_URL = "https://simonwillison.net/entries/"
SIMON_WILLISON_BASE_URL = "https://simonwillison.net"
COLLECTION_NAME = "simon_willison_blog"


def parse_simon_willison_date(date_str: str) -> str:
    """
    Parse Simon Willison's date format like "30th March 2026" or "27th March 2026"
    and convert to ISO 8601 format (YYYY-MM-DD).

    :param date_str: Date string from Simon Willison's blog
    :return: ISO formatted date string (YYYY-MM-DD)
    """
    try:
        # Remove ordinal suffixes (st, nd, rd, th)
        # The date format is like "30th March 2026"
        # Split to get the day, month, and year
        parts = date_str.split()
        if len(parts) >= 3:
            day_part = parts[0]  # e.g., "30th"
            month_part = parts[1]  # e.g., "March"
            year_part = parts[2]  # e.g., "2026"

            # Remove ordinal suffix from day (st, nd, rd, th) - need to check each
            day_clean = day_part
            for suffix in ["st", "nd", "rd", "th"]:
                if day_clean.endswith(suffix):
                    day_clean = day_clean[: -len(suffix)]
                    break

            # Convert to integer and back to string to remove leading zeros if any
            day = int(day_clean)

            # Parse month name to number
            month = datetime.strptime(month_part, "%B").month

            # Format as YYYY-MM-DD
            return f"{year_part}-{month:02d}-{day:02d}"

        return date_str
    except Exception as e:
        logger.warning(f"Failed to parse Simon Willison date '{date_str}': {e}")
        return date_str


class SimonWillisonBlogParser(WebParser):
    def parse(self, resp_text: str) -> List[dict]:
        soup = BeautifulSoup(resp_text, "lxml")

        # Find all blog post entries
        blog_list = []
        for entry_div in soup.find_all("div", class_="entry segment"):
            post = self._parse_item(entry_div)
            if post:
                blog_list.append(post)

        logger.info(f"{len(blog_list)} simon willison blog posts parsed")
        return blog_list

    def _parse_item(self, entry_div) -> dict:
        try:
            # Extract title and URL from h3 tag
            h3 = entry_div.find("h3")
            if not h3:
                return None

            link = h3.find("a")
            if not link:
                return None

            title = link.get_text(strip=True)
            href = link.get("href", "")
            if not href:
                return None

            # All URLs are relative, prepend base URL
            url = f"{SIMON_WILLISON_BASE_URL}{href}"

            # Extract date from entryFooter
            # The date is in format like "2:28 pm / 30th March 2026"
            entry_footer = entry_div.find("div", class_="entryFooter")
            if not entry_footer:
                return None

            # Get all links in entry footer to find the date link
            footer_links = entry_footer.find_all("a")
            created_at = None

            for footer_link in footer_links:
                link_text = footer_link.get_text(strip=True)
                # The date link looks like "30th March 2026"
                if (
                    "March" in link_text
                    or "April" in link_text
                    or "May" in link_text
                    or "June" in link_text
                    or "July" in link_text
                    or "August" in link_text
                    or "September" in link_text
                    or "October" in link_text
                    or "November" in link_text
                    or "December" in link_text
                    or "January" in link_text
                    or "February" in link_text
                ):
                    created_at = parse_simon_willison_date(link_text)
                    break

            if not created_at:
                logger.warning(f"No date found in entry footer for: {title}")
                return None

            return {
                "id": title,
                "url": url,
                "created_at": created_at,
                "crawled_at": datetime.now().strftime("%Y%m%d%H%M%S"),
            }
        except Exception as e:
            logger.warning(f"Failed to parse simon willison blog item: {e}")
            return None


def crawl():
    parser = SimonWillisonBlogParser()
    web_crawler.crawl(
        parser, SIMON_WILLISON_BLOG_URL, COLLECTION_NAME, proxies=config["proxies"]
    )


if __name__ == "__main__":
    crawl()
