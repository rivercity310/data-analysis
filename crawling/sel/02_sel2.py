import requests
from sel_options import get_chrome_driver, DEFAULT_PATH
from selenium.webdriver.common.by import By


driver = get_chrome_driver(bypass=True, download=True)

if driver:
    addr = input("주소를 입력하세요: ")
    driver.get(addr)

    domain = addr[(addr.rindex("/") + 1):addr.rindex(".")]
    page_numbers_elem = driver.find_elements(by=By.CLASS_NAME, value="page-numbers")
    driver.implicitly_wait(3)

    for page_index, page_number_elem in enumerate(page_numbers_elem):
        page_number_elem.click()
        driver.implicitly_wait(3)
        me = driver.find_elements(by=By.CLASS_NAME, value="gen-movie-info")
        mi = driver.find_elements(by=By.CLASS_NAME, value="gen-movie-img")

        print(f"{page_index}페이지 작업중........")

        for idx, i in enumerate(mi):
            i_tag = i.find_element(by=By.TAG_NAME, value="img")
            src = i_tag.get_attribute("src")
            alt = i_tag.get_attribute("alt")

            if not src or not alt:
                continue

            with open(f"{DEFAULT_PATH}({alt}){src.split('/')[-1]}", "wb") as f:
                res = requests.get(src)
                if res.ok:
                    print(f"{alt}: {src}")
                    f.write(res.content)

                driver.implicitly_wait(2)

        with open(f"{DEFAULT_PATH}cp_{domain}_info_{page_index}.txt", "wt") as f:
            for m in me:
                a_tag = m.find_element(by=By.TAG_NAME, value="a")
                href = a_tag.get_attribute("href")
                title = a_tag.text
                f.writelines(f"{title}: {href}")
                f.writelines("\n")

        driver.get_screenshot_as_file(f"{DEFAULT_PATH}cp_{domain}_page_{page_index}.png")
        # print(driver.page_source)
        print("-"*100)

    driver.delete_network_conditions()
    driver.delete_all_cookies()
    driver.quit()
