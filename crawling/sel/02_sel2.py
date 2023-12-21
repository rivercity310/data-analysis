import requests
import os
import logging.config
from sel_options import get_chrome_driver, DEFAULT_PATH
from selenium.webdriver.common.by import By


def crawling_images_and_links():
    driver = get_chrome_driver(bypass=True, download=True, headless=True)

    if driver:
        addr = input("주소를 입력하세요: ")
        driver.get(addr)

        domain = addr[(addr.rindex("/") + 1):addr.rindex(".")]
        page_numbers_elem = driver.find_elements(by=By.CLASS_NAME, value="page-numbers")
        driver.implicitly_wait(3)

        remove_list = []

        try:
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

                    file_path = f"{DEFAULT_PATH}({alt}){src.split('/')[-1]}"

                    with open(file_path, "wb") as f:
                        res = requests.get(src)

                        if res.status_code == requests.codes.OK:
                            print(f"{alt}: {src}")
                            f.write(res.content)
                        elif res.status_code == requests.codes.FORBIDDEN:
                            remove_list.append(file_path)

                # page 정보 Scrapping
                page_raw_info = "{}cp_{}_{}_{}.{}"
                page_info_path = page_raw_info.format(DEFAULT_PATH, domain, "info", page_index, "txt")
                remove_list.append(page_info_path)

                with open(page_info_path, "wt") as f:
                    for m in me:
                        a_tag = m.find_element(by=By.TAG_NAME, value="a")
                        href = a_tag.get_attribute("href")
                        title = a_tag.text
                        f.writelines(f"{title}: {href}")
                        f.writelines("\n")

                page_screenshot_path = page_raw_info.format(DEFAULT_PATH, domain, "screenshot", page_index, "png")
                driver.get_screenshot_as_file(page_screenshot_path)
                remove_list.append(page_screenshot_path)

                print("-" * 100)

        except Exception as e:
            logging.config.fileConfig("../../logging.conf")
            logger = logging.getLogger(__name__)
            logger.critical(e)
            raise e

        finally:
            driver.delete_network_conditions()
            driver.delete_all_cookies()
            driver.quit()

            for remv in remove_list:
                os.remove(remv)

            del remove_list


if __name__ == "__main__":
    crawling_images_and_links()
