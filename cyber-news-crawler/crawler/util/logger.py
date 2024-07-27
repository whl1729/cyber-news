"""This module provides logging functionality."""
import logging
from logging.handlers import RotatingFileHandler

from util.fs import log_dir
from util.fs import log_path
from util.argparser import args

def init_logger(log_level: str):
    logger = logging.getLogger("helloworld")
    log_level = log_level.upper()
    logger.setLevel(log_level)

    log_dir.mkdir(exist_ok=True)

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d: %(message)s"
    )
    file_handler = RotatingFileHandler(log_path, maxBytes=1048576, backupCount=100)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(log_level)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(log_level)
    logger.addHandler(console_handler)
    logger.info("Successfully initialized the logger")
    return logger


logger: logging.Logger = init_logger(args.log_level)
