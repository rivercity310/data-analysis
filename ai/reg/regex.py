import requests
import re

r'''
^ : 문자열의 시작
$ : 문자열의 끝
. : 한 개의 문자
\d : 한 개의 숫자
\w : 한 개의 문자나 숫자
\W : 한 개의 문자나 숫자가 아닌 것
\s : 공백문자 (스페이스, 탭, 줄바꿈 등)
\S : 공백문자가 아닌 것
* : 0회 이상 반복
+ : 1회 이상 반복
[abc] : a, b, c 중 하나
[^abc] : a, b, c가 아닌 어떤 문자
a|b : a 또는 b
? : 0회 또는 1회 반복
'''


def _request_get_page(url: str) -> str:
    res = requests.get(url)

    if res.status_code == requests.status_codes.codes.OK:
        print(res.content)
        return str(res.content.strip())
    else:
        raise Exception


def _find_pattern_str(regex: str, dst_str: str) -> set[str]:
    return set(re.findall(regex, dst_str))


if __name__ == "__main__":
    url = "https://youtube.com"
    page_str = _request_get_page(url)

    # regex = r"\([0-9]+\)"         # (숫자) 패턴
    regex = r"https*://[/|\w|.|-|\?|&|=]+"
    print(_find_pattern_str(regex, page_str))
