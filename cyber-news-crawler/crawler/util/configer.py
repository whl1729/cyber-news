from dotenv import load_dotenv
import os
import yaml

from crawler.util import fs
from crawler.util.logger import logger

class Configer:
    def __init__(self, file_path: str):
        self._file_path = file_path
        self._config = self._load_config()

        load_dotenv()
        self._config["github_username"] = os.getenv("GITHUB_USERNAME")
        self._config["github_password"] = os.getenv("GITHUB_PASSWORD")

    def _load_config(self):
        config_path = fs.config_dir / self._file_path
        with open(config_path, "r") as file:
            config = yaml.safe_load(file)
        logger.info("Successfully loaded project config")
        return config

    def get_config(self):
        return self._config

config = Configer("crawler_config.yaml").get_config()
