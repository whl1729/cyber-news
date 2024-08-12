import argparse


def parse_args():
    argparser = argparse.ArgumentParser(
        "cyber-news-crawler",
        description="crawl news on the Internet",
    )
    argparser.add_argument(
        "-l",
        "--log-level",
        default="info",
        help="log level. Value: debug, info, warn or error",
    )
    args = argparser.parse_args()
    print("Successfully parsed command-line arguments")
    return args


args = parse_args()

if __name__ == "__main__":
    print(f"log_level: {args.log_level}, args: {args}")
