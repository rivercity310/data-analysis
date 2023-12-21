from sel_options import get_chrome_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import logging.config
import time
import json


# 3:15:00

GET_PATH = "http://naver.com"
LOGIN_BTN_XPATH = "//*[@id=\"account\"]/div/a"
LOGGING_CONF_PATH = "../../logging.conf"
driver = None


def _get_login_info_from_drive() -> tuple:
    path = "D:\\login_info.json"

    with open(path, "r") as f:
        info = json.load(f)
        print(info)

        return info['id'], info['pw']


def auto_login_to_naver():
    global driver

    try:
        driver = get_chrome_driver()
        driver.get(GET_PATH)

        login_btn_elem = driver.find_element(by=By.XPATH, value=LOGIN_BTN_XPATH)
        login_btn_elem.click()

        input_id_elem = driver.find_element(by=By.ID, value="id")
        input_pwd_elem = driver.find_element(by=By.ID, value="pw")
        sign_in_btn_elem = driver.find_element(by=By.ID, value="log.login")

        (login_id, login_pw) = _get_login_info_from_drive()

        input_id_elem.send_keys(login_id)
        input_pwd_elem.send_keys(login_pw)
        sign_in_btn_elem.send_keys(Keys.ENTER)

        time.sleep(10)

        # 서버에서 자동 로그인 감지 시 captcha 발생: 2captcha 라이브러리를 활용하여 해결

    except Exception as e:
        logging.config.fileConfig(LOGGING_CONF_PATH)
        logger = logging.getLogger(__name__)
        logger.critical(e)

    finally:
        if driver:
            driver.delete_network_conditions()
            driver.delete_all_cookies()
            driver.quit()


if __name__ == "__main__":
    auto_login_to_naver()
