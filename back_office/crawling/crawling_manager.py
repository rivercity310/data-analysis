import requests
from bs4 import BeautifulSoup


class CrawlingManager:

    def __init__(self):
        url = input("크롤링할 사이트의 주소를 입력해주세요: ")
        req = requests.get(url)

        if req.ok:
            print(f"{url} 응답 완료..")
            self.soup = BeautifulSoup(req.text, "html.parser")
            print("HTML parsing OK")
        
        else:
            print(f"{url} 요청에 실패하였습니다.")
            print("프로그램을 종료합니다.")
            return


if __name__ == "__main__":
    cm = CrawlingManager()
        