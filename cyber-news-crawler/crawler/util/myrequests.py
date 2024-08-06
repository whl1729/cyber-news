import requests
from crawler.util.logger import logger


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
