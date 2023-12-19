import requests

# HTTP GET 요청
url = "https://github.com/rivercity310"
res = requests.get(url)

# if res.status_code == requests.codes.ok:
#    print("정상")

# 응답코드가 200이 아니면 에러 raise (더이상 진행 안됨)
res.raise_for_status()

# 가져온 html을 파일에 쓰기
path = "C:/Users/seungsu/Desktop/mygit.html"
with open(path, "w", encoding="utf-8") as f:
    f.write(res.text)


