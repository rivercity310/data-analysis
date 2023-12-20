from selenium import webdriver
from selenium.webdriver.common.by import By


DEFAULT_PATH = "D:\\selenium\\"


def get_chrome_driver(bypass: bool = False, download: bool = False) -> webdriver.Chrome:
    """ Chrome Driver 생성, 옵션 설정

    :param bypass: IP 우회 옵션 설정
    :param download: 다운로드 기능 ON/OFF

    :return: Chrome Driver 객체
    """
    chrome_options = _set_selenium_options(bypass, download)
    driver = webdriver.Chrome(options=chrome_options)
    return driver


def _set_selenium_options(bypass: bool = False, download: bool = False) -> webdriver.ChromeOptions:
    """ Selenium 옵션을 설정하고, 설정값을 담고있는 ChromeOptions 객체 반환

    :return: 설정된 Chrome 옵션 객체
    """
    options = webdriver.ChromeOptions()

    # headless 옵션 설정
    options.add_argument("headless")        # 브라우저가 뜨지 않고 실행됨 (Background 실행)
    options.add_argument("no-sandbox")

    options.add_argument("window-size=1920x1080")       # 브라우저 윈도우 사이즈 설정
    options.add_argument("disable-gpu")                 # 가속 사용 X
    options.add_argument("lang=ko_KR")                  # 가짜 플러그인 탑재

    if bypass:
        options.add_argument("--proxy-server=socks5://127.0.0.1:9150")  # IP 우회
        options.add_argument("incognito")       # Secret 모드
    else:
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        options.add_argument(f"User-Agent={user_agent}")    # User-Agent 설정

    if download:
        options.add_experimental_option("prefs", {
            "download.default_directory": DEFAULT_PATH[:-2],
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
        })

    return options


def _find_my_public_ip() -> str:
    driver = webdriver.Chrome()
    driver.get("https://icanhazip.com")
    driver.implicitly_wait(5)

    tds = driver.find_element(by=By.TAG_NAME, value="pre")
    return tds.text


if __name__ == "__main__":
    _find_my_public_ip()
