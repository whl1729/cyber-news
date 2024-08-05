from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def verify_device():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    browser = webdriver.Chrome(options=chrome_options)

    try:
        browser.get("https://github.com/login")
        input = browser.find_element(By.ID, "otp")
        input.send_keys("320817")
        button = browser.find_element(By.CLASS_NAME, "btn-primary btn btn-block")
        button.send_keys(Keys.ENTER)
        wait = WebDriverWait(browser, 10)
        wait.until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "AppHeader-context-item-label")
            )
        )
        print(browser.current_url)
        print(browser.get_cookies())
        print(browser.page_source)
    except Exception as e:
        print(f"verify device throws: {e}")
    finally:
        browser.close()


if __name__ == "__main__":
    verify_device()
