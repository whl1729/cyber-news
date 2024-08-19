"""
This module manages the file path for the project.
"""
import json
import sys
from pathlib import Path

bin_dir: Path = (
    Path(sys.executable).parent
    if hasattr(sys, "frozen")
    else Path(__file__).parent.parent
)

project_dir: Path = bin_dir.parent
env_path: Path = project_dir / ".env"
config_dir: Path = project_dir / "config"
log_dir: Path = project_dir / "log"
log_path: str = str(log_dir / "crawler_log.txt")

log_dir.mkdir(exist_ok=True)


def save_log(content: str, dest_path: str):
    with open(log_dir / dest_path, "w", encoding="utf-8") as f:
        f.write(content)


def save_json(content: object, dest_path: str):
    if isinstance(content, str):
        content = json.loads(content)

    with open(log_dir / dest_path, "w", encoding="utf-8") as f:
        json.dump(content, f, indent=4, ensure_ascii=False)
