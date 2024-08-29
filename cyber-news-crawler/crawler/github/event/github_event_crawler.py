from crawler.github.event.github_user_event_crawler import GithubUserEventCrawler


def main():
    user_event_crawler = GithubUserEventCrawler()
    user_event_crawler.crawl()


if __name__ == "__main__":
    main()
