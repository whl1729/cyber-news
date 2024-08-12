from crawler.util import fs
from crawler.util.logger import logger
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# 1 hour
LOAD_TIMEOUT = 3600


def verify_device():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_page_load_timeout(LOAD_TIMEOUT)

    try:
        driver.get("https://github.com/login")
        input_element = WebDriverWait(driver, LOAD_TIMEOUT).until(
            EC.visibility_of_element_located((By.ID, "otp"))
        )
        logger.info("input element located")
        verification_code = input("Please enter device verification code:\n")
        input_element.send_keys(verification_code)
        button = driver.find_element(By.CLASS_NAME, "btn-primary btn btn-block")
        button.send_keys(Keys.ENTER)
        WebDriverWait(driver, LOAD_TIMEOUT).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "AppHeader-context-item-label")
            )
        )
        fs.save(driver.page_source, "verified.html")
        logger.info("current_url:", driver.current_url)
        logger.info("cookies:", driver.get_cookies())
        logger.info("verify device ok")
    except Exception as e:
        logger.error(f"verify device throws: {e}")
    finally:
        driver.close()


if __name__ == "__main__":
    verify_device()