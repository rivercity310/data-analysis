import re

# re 모듈 공식 메뉴얼: https://docs.python.org/3.7/library/re.html
# re 적용 예제 문서: https://docs.python.org/3.7/howto/regex.html#regex-howto

if __name__ == "__main__":
    text = "My id number is [G203_5A]"

    print(re.findall('a', text))   # 소문자 'a' 찾기
    print(re.findall('A', text))   # 대문자 'A' 찾기
    print(re.findall('i', text))   # 소문자 'i' 찾기

    # 문자의 범위로 검색하기
    print(re.findall('[a-z]', text))      # 소문자 찾기: ['y', 'i', 'd', ... ]
    print(re.findall('[a-z]+', text))     # 소문자 연속해서 찾기: ['y', 'id', 'number', ... ]
    print(re.findall('[A-Z]', text))      # 대문자 찾기
    print(re.findall('[0-9]', text))      # 숫자 찾기
    print(re.findall('[0-9]+', text))     # 숫자 연속해서 찾기

    # 여러 패턴
    print(re.findall('[a-zA-Z0-9]', text))      # 영문자 및 숫자 찾기
    print(re.findall('[a-zA-Z0-9]+', text))     # 영문자 및 숫자 연속해서 찾기
    print(re.findall('[^a-zA-Z0-9]', text))     # 영문자 및 숫자 아닌 문자 찾기
    print(re.findall('[\w]', text))             # \w (word): 알파벳, 숫자, '_'에 해당하는 문자
    print(re.findall('[\w]+', text))            # 즉, [\w] = [0-9a-zA-Z_]
    print(re.findall('[\W]', text))             # \W (non-word): 알파벳, 숫자, '_'가 아닌 문자
