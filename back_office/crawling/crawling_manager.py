import os
import json
import time
import sys
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pathlib import Path


class CrawlingManager:
    _crawling_dir_path = Path(__file__).parent

    _patch_file_path = _crawling_dir_path / "patchfiles"

    _json_file_path = _crawling_dir_path / "result.json"

    _chrome_driver_path = _crawling_dir_path / "chromedriver.exe"


    def __init__(self):
        # patchfiles 폴더 비어있는지 검사 
        while True:
            if len(os.listdir(self._patch_file_path)) == 0:
                break
            input(f"{self._patch_file_path} 폴더를 비우고 <Enter>를 입력하세요.")
        
        
        url = input("크롤링할 사이트의 주소를 입력해주세요: ")

        # 다운로드 경로 설정
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        options.add_experimental_option("prefs", {
            "download.default_directory": str(self._patch_file_path)
        })
        
        # selenium 버전 높은 경우 -> executable_path Deprecated -> Service 객체 사용
        try:
            self.driver = webdriver.Chrome(options = options, service = Service(executable_path = self._chrome_driver_path))
        except Exception as _:
            print("[ERR] 구버전 webdriver로 동작합니다.")
            self.driver = webdriver.Chrome(executable_path = str(self._chrome_driver_path), options = options)
        
        # Get 요청 후 HTML 파싱
        self.driver.get(url)
        self._load_all_page()
        self.soup = BeautifulSoup(self.driver.page_source, "html.parser")
        
        print("HTML parsing OK")


    def _wait_til_download_ended(self):
        while True: 
            dl = False
            for file in os.listdir(self._patch_file_path):
                if file.endswith("crdownload"):
                    dl = True

            print("아직 파일을 다운로드 하고있어요...............")
            time.sleep(2)

            if not dl:
                break


    def _save_result(self, result_dict: dict):
        with open(str(self._json_file_path), "w", encoding = "utf8") as fp:
            json.dump(
                obj = result_dict, 
                fp = fp, 
                indent = 4,
                sort_keys = True, 
                ensure_ascii = False
            )


    # 동적 페이지의 경우 로딩을 위해 전체 페이지 탐색 
    def _load_all_page(self):
        chains = ActionChains(self.driver)

        for _ in range(10):
            chains.send_keys(Keys.PAGE_DOWN).perform()
            time.sleep(0.5)

        chains.send_keys(Keys.HOME).perform()
        time.sleep(1)


    def _driver_wait(self, by: By, name: str):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((by, name)),
                f"[ERR] Can't Find {by}, {name}"            
            )

        except Exception as e:
            print(e)
            self._del_driver()


    def _del_driver(self):
        try:
            del self.soup
            del self.driver
            del self
        
        except Exception as _:
            print("[ERR] 메모리 해제 작업...")
            return
        
        finally:
            print("프로그램을 종료합니다....")


if __name__ == "__main__":
    cm = CrawlingManager()