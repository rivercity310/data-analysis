from sel_options import get_chrome_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


driver = get_chrome_driver(bypass=True)

if driver:
    addr = input("주소를 입력하세요: ")
    driver.get(addr)

    me = driver.find_elements(by=By.CLASS_NAME, value="gen-movie-info")

    for m in me:
        a_tag = m.find_element(by=By.TAG_NAME, value="a")
        href = a_tag.get_attribute("href")
        title = a_tag.text
        print(f"{title}: {href}")

    driver.delete_network_conditions()
    driver.delete_all_cookies()
    driver.quit()
