import requests
import csv
from bs4 import BeautifulSoup

url = "https://finance.naver.com/sise/sise_market_sum.nhn?sosok=0&page="
filename = "시가총액1-200.csv"
f = open(filename, "w", encoding="utf-8-sig", newline="")
writer = csv.writer(f)

title = "N 종목명 현재가 전일비 등락률 액면가 시가총액 상장주식수 외국인비율 거래량 PER ROE".split(" ")
writer.writerow(title)

for page in range(1, 5):
    res = requests.get(url + str(page))
    res.raise_for_status()

    soup = BeautifulSoup(res.text, "lxml")
    data_rows = soup.find("table", attrs={"class": "type_2"}).find("tbody").find_all("tr")

    for row in data_rows:
        columns = row.find_all("td")
        if len(columns) <= 1:   # 의미없는 데이터 skip
            continue

        data = [column.get_text().strip() for column in columns]

        # PER N/A 또는 20이하만 추가
        if data[10] == 'N/A' or float(data[10]) <= 20:
            writer.writerow(data)
