"""
This module manages the file path for the project.
"""
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

bin_dir: Path = (
    Path(sys.executable).parent
    if hasattr(sys, "frozen")
    else Path(__file__).parent.parent
)

project_dir: Path = bin_dir.parent
news_dir: Path = project_dir / "news"
env_path: Path = news_dir / ".env"

config_dir: Path = project_dir / "config"
log_dir: Path = project_dir / "log"
log_path: str = str(log_dir / "cyber_news_log.txt")
log_dir.mkdir(exist_ok=True)

load_dotenv(env_path)
post_dir: Path = Path(os.getenv("CYBER_NEWS_POST_DIR"))
post_dir.mkdir(exist_ok=True)


def save_response_text(content: str, filename: str):
    if "<html" in content:
        save_text(content, filename + ".html")
        return

    try:
        save_json(content, filename + ".json")
    except Exception:
        save_text(content, filename + ".txt")


def save_text(content: str, dest_path: str):
    with open(log_dir / dest_path, "w", encoding="utf-8") as f:
        f.write(content)


def save_json(content: str, dest_path: str):
    content = json.loads(content)

    with open(log_dir / dest_path, "w", encoding="utf-8") as f:
        json.dump(content, f, indent=4, ensure_ascii=False)


def save_post(content: str, filename: str):
    with open(post_dir / filename, "w", encoding="utf-8") as f:
        f.write(content)
