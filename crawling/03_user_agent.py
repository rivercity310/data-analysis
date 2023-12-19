import requests

# HTTP header의 user-agent 속성을 통해
# 서버에서 접속한 사용자의 정보를 알 수 있음 (접속 기기, 브라우저 정보 등)

# 크롤링 시도 시 403이 뜨는 경우 User-Agent 속성을 세팅하여 해결 가능
url = "http://nadocoding.tistory.com"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
path = "C:/Users/seungsu/Desktop/nadocoding.html"

res = requests.get(url, headers)
res.raise_for_status()

with open(path, "w", encoding="utf8") as f:
    print(res.text)
    f.write(res.text)