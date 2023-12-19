import re

# . : 하나의 문자 의미 (ca.e -> cafe, case, (o) | caffe(x))
# ^ : 문자열의 시작을 의미 (^de -> de로 시작하는 문자열)
# $ : 문자열의 끝을 의미 (se$ -> case, base (o) | face(x))

# 1. 정규식을 컴파일하여 패턴 객체를 얻음
p = re.compile("ca.e")


def print_match(m):
    if m:
        print(f"m.group(): {m.group()}")    # group(): 일치하는 문자열 반환
        print(f"m.string: {m.string}")      # string: 입력받은 문자열
        print(f"m.start: {m.start()}")      # start(): 일치하는 문자열의 시작 index
        print(f"m.end: {m.end()}")          # end(): 일치하는 문자열의 끝 index
        print(f"m.span(): {m.span()}")      # span(): 일치하는 문자열의 시작/끝 index
    else:
        print("매칭되지 않음")


# match: 주어진 문자열의 처음부터 일치하는지 확인
m = p.match("case")
print_match(m)
del m

# search: 주어진 문자열 중에 일치하는게 있는지 확인
m = p.search("good care")
print_match(m)
del m

# findall: 일치하는 모든 것을 리스트 형태로 반환
lst = p.findall("careless cafe")
print(lst)
del lst
