import os

import yaml
from dotenv import load_dotenv

from news.util import fs
from news.util.logger import logger


class Configer:
    def __init__(self, file_path: str):
        self._file_path = file_path
        self._config = self._load_config()

        load_dotenv()
        self._merge_env()

    def _merge_env(self):
        self._config["github_username"] = os.getenv("GITHUB_USERNAME")
        self._config["github_password"] = os.getenv("GITHUB_PASSWORD")
        self._config["github_token"] = os.getenv("GITHUB_TOKEN")
        self._config["exmail_server"] = os.getenv("EXMAIL_SERVER")
        self._config["exmail_user"] = os.getenv("EXMAIL_USER")
        self._config["exmail_password"] = os.getenv("EXMAIL_PASSWORD")
        self._config["mongodb_host"] = os.getenv("MONGODB_HOST", "127.0.0.1")
        self._config["mongodb_port"] = os.getenv("MONGODB_PORT", 27017)
        self._config["mongodb_database"] = os.getenv("MONGODB_DATABASE", "newsDB")
        self._config["chromedriver_path"] = os.getenv(
            "CHROMEDRIVER_PATH", "/usr/local/bin/chromedriver"
        )

        proxy_url = os.getenv("PROXY_URL")
        proxies = {"http": proxy_url, "https": proxy_url}
        self._config["proxies"] = proxies

    def _load_config(self):
        config_path = fs.config_dir / self._file_path
        with open(config_path, "r") as file:
            config = yaml.safe_load(file)
        logger.info("Successfully loaded project config")
        return config

    def get_config(self):
        return self._config


config = Configer("cyber_news_config.yaml").get_config()
