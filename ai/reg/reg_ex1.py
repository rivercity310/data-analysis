import re


# https://greeksharifa.github.io/%EC%A0%95%EA%B7%9C%ED%91%9C%ED%98%84%EC%8B%9D(re)/2018/07/28/regex-usage-04-intermediate/

def ex1():
    text = """
        101 COM Python
        102 MAT LinearAlgebra
        103 ENG ComputerArchitecture
    """
    pattern = re.compile(r"\d+")
    print(pattern.findall(text.strip()))
    print(pattern.search(text.strip()).groups())

    # 1. re.compile을 통해 Pattern 객체를 얻는다. (매개변수: regex)
    # 2-1. pattern.findall(text) -> 정규식에 일치하는 모든 부분 문자열 반환
    # 2-2. pattern.search(text)  -> 정규식에 첫번째로 일치하는 Match 객체 반환
    # 3-1. match.group() -> 정규식 전체의 일치부 반환 (첫번째 일치하는 문자열만), 인수를 통해 i번째 캡쳐된 캡쳐 문자열에 접근 가능
    # 3-2. match.groups() -> 명시적으로 캡쳐한(소괄호로 감싼) 부분 반환
    pattern2 = re.compile(r"\w+")
    print(pattern2.search(text).group())        # 제일 먼저 발견되는 101 반환
    print(pattern2.findall(text))

    text3 = "1999/05/21 2018-07-28 2018-06-31 2019.01.01"
    pattern3 = re.compile(r"\d{4}-(\d?\d)-(\d?\d)")     # 소괄호 캡쳐 기능 사용 (해당 부분만 추출)
    match_obj = pattern3.search(text3)
    print(match_obj.group(0))                           # = .group(), 첫번째로 일치하는 부분 문자열 반환 -> 2018-07-28
    print(match_obj.group(1))                           # 첫번째 캡쳐된 부분 반환 -> 07
    print(match_obj.group(2))                           # 두번째 캡쳐된 부분 반환 -> 28
    print(match_obj.groups())                           # 캡쳐된 부분 전체를 튜플 형식으로 반환 -> ('07', '28')





if __name__ == "__main__":
    ex1()
