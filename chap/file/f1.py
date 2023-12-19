import json

# [ JSON 활용 ]
my_info = {'name': 'seungsu', 'job': 'programmer', 'lang': ['Java', 'Python', 'Kotlin']}

# 1. Serializing
print(json.dumps(my_info))

# 2. 직렬화 동시에 파일 입력
desktop = "C:/Users/seungsu/Desktop/"
path = desktop + "my_info2.json"
with open(path, "w") as f:
    json.dump(my_info, f)

with open(path, "r") as fr:
    # 역직렬화
    print(json.load(fr))

# 3. 한글 데이터 저장 (ASCII/Unicode 저장 모드 끄기)
books = [{'제목': 'Python', '출판연도': '2023-12-19'}]
del path
path = desktop + "books.json"

with open(path, "w") as f:
    json.dump(books, f, ensure_ascii=False)

with open(path, "r") as f:
    print(json.load(f))
