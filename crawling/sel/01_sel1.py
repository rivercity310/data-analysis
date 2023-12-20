from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys     # Keys.Enter()
from sel_options import get_chrome_driver

# selenium 설치: python -m pip install selenium
# chromedriver: Chrome 제어 드라이버


# [ 탐색 ]
driver = get_chrome_driver()
driver.get("https://naver.com")
driver.implicitly_wait(3)      # 렌더링이 될 때까지 3초 대기

# python 3.7 이상 버전: find_element       By 속성으로 지정
# 그 이하 버전: find_elements_by
# elem = browser.find_element(by=)       # element 객체 가져오기
''' 
[By 속성] from selenium.webdriver.common.by import By
ID = "id"
XPATH = "xpath"
LINK_TEXT = "link text"
PARTIAL_LINK_TEXT = "partial link text"
NAME = "name"
TAG_NAME = "tag name"
CLASS_NAME = "class name"
CSS_SELECTOR = "css selector"
'''

# 캡쳐 파일 저장 경로
file_path = "D:\\selenium\\"

# WebElement 객체 가져오기 (로그인 버튼)
elem = driver.find_element(by=By.CLASS_NAME, value="MyView-module__link_login___HpHMW")

elem.click()        # 찾은 Element 클릭
driver.back()      # 이전 페이지로 이동
driver.forward()   # 다음 페이지로 이동
driver.refresh()   # 새로고침
driver.get_screenshot_as_file(f"{file_path}login.png")     # 화면 캡쳐
driver.back()

del elem

# 검색창 Element 객체 가져오기
query_elem = driver.find_element(by=By.CLASS_NAME, value="search_input")
query_elem.send_keys("수락산역 맛집")
query_elem.send_keys(Keys.ENTER)     # Keys.ENTER를 위해 Keys 모듈 import
driver.get_screenshot_as_file(f"{file_path}search_result.png")

del query_elem

# 여러 WebElement 객체 가져오기
a_elements = driver.find_elements(by=By.TAG_NAME, value="a")

for a_tag in a_elements:
    href = a_tag.get_attribute("href")      # 속성값 가져오기
    print(href)

driver.quit()      # driver 종료
