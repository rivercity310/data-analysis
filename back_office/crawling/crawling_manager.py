from bs4 import BeautifulSoup
from selenium import webdriver


class CrawlingManager:
    def __init__(self, test_link = None):
        url = input("크롤링할 사이트의 주소를 입력해주세요: ")

        # 다운로드 경로 설정
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--disable-popup-blocking")
        self.options.add_argument("--disable-extensions")
        self.options.add_argument("--disable-gpu")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        self.options.add_experimental_option("prefs", {
            "download.default_directory": "D:\\patch\\patchfiles"
        })

        self.browser = webdriver.Chrome(
            executable_path = r"C:\Users\seungsu\Desktop\projects\unittest\chromedriver.exe",
            options = self.options
        )
        
        self.browser.get(url)
        self.browser.implicitly_wait(5)
        self.soup = BeautifulSoup(self.browser.page_source, "html.parser")

        print("HTML parsing OK")

    
    def get_new_browser_obj(self):
        return webdriver.Chrome(
            executable_path = r"C:\Users\seungsu\Desktop\projects\unittest\chromedriver.exe",
            options = self.options
        )


if __name__ == "__main__":
    cm = CrawlingManager()
        