"""
This module manages the file path for the project.
"""
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
