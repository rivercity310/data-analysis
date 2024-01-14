import requests
from bs4 import BeautifulSoup
from selenium import webdriver


class CrawlingManager:

    def __init__(self, test_link = None):
        if test_link == None:
            url = input("크롤링할 사이트의 주소를 입력해주세요: ")
            req = requests.get(url)
        else:
            req = requests.get(test_link)

        self.browser = webdriver.Chrome(r"C:\Users\seungsu\Desktop\projects\unittest\chromedriver.exe")

        if not req.ok:
            print(f"{url} 요청에 실패하였습니다.")
            print("프로그램을 종료합니다.")
            return

        self.soup = BeautifulSoup(req.text, "html.parser")
        print("HTML parsing OK")
        

if __name__ == "__main__":
    cm = CrawlingManager()
        