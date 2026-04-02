import argparse


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        "cyber-news",
        description="update daily technology news",
    )
    parser.add_argument(
        "-l",
        "--log-level",
        default="info",
        help="log level. Value: debug, info, warn or error",
    )
    parser.add_argument(
        "-t",
        "--topic",
        default=None,
        help="Specific topic to crawl (e.g., harrison_chase_blog)",
    )
    return parser.parse_args()


args = parse_args()
