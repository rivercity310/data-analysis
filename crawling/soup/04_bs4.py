import requests
from bs4 import BeautifulSoup

url = "https://comic.naver.com/webtoon/weekday.nhn"
res = requests.get(url)
res.raise_for_status()

# lxml 파서를 통해 전달된 구문 분석
soup = BeautifulSoup(res.text, "lxml")

# 첫번째로 발견되는 태그 가져오기
print(soup.title)               # title 태그와 내용 가져오기
print(soup.title.get_text())    # title 태그 안 내용만 가져오기
print(soup.script.get_text())
print(soup.meta.attrs)          # meta 태그가 가진 속성 정보 사전 형태로 출력
print(soup.meta["charset"])     # 원하는 속성 값만 가져오기

# 조건에 만족하는 첫번째 태그 가져오기
print(soup.find("meta", attrs={"property": "og:image"}))
print(soup.find(attrs={"id": "root"}))      # 태그를 생략해도 됨

del url, res, soup
print("-" * 60)

url = "https://comic.naver.com/webtoon/detail?titleId=819217&no=8&week=tue"
res = requests.get(url)
res.raise_for_status()

soup = BeautifulSoup(res.text, "lxml")
titles = soup.find_all("p", attrs={"class": "title"})

for title in titles:
    print(title.get_text().strip())

