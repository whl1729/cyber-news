from dataclasses import dataclass

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from news.util.configer import config
from news.util.logger import logger


@dataclass
class MyResponse:
    status_code: int
    text: str


def get(url, params=None, max_try=10, **kwargs):
    for i in range(max_try):
        try:
            response = requests.get(url, params, **kwargs)
            if response.status_code == 200:
                return response
            logger.warn(
                f"{i+1}. Failed to get {url}. Status Code: {response.status_code}"
            )
        except Exception as e:
            logger.error(f"{i+1}. Failed to get {url}. Exception: {e}")

    return None


def get_with_selenium(url, max_try=10, **kwargs):
    # 可选：配置 Chrome 选项
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 无头模式，不打开浏览器界面
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--ignore-certificate-errors")  # 忽略证书错误
    chrome_options.add_argument("--disable-dev-shm-usage")

    # 初始化 ChromeDriver
    service = Service(config["chromedriver_path"])
    browser = None

    for i in range(max_try):
        try:
            browser = webdriver.Chrome(service=service, options=chrome_options)
            browser.get(url)
            return MyResponse(status_code=200, text=browser.page_source)
        except Exception as e:
            logger.error(f"{i+1}. Failed to get {url} with selenium. Exception: {e}")
            return MyResponse(status_code=500, text="")
        finally:
            if browser:
                browser.quit()
