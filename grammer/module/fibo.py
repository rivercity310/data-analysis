# 피보나치 수열을 위한 모듈

def fib(n):
    a, b = 0, 1
    while b < n:
        print(b, end=' ')
        a, b = b, a + b
    print()


def fib2(n):
    result = []
    a, b = 0, 1
    while b < n:
        result.append(b)
        a, b = b, a + b

    return result


def _test():
    print("test!")


# 외부에서 호출 시
# __name__이 __main__이라는 뜻은 파이썬 외부에서 호출되었다는 의미
# sys 모듈은 시스템 관련 모듈이며, sys.argv라는 리스트를 통해 시스템 상에 입력된 인자 값을 불러올 수 있다.
# cmd: python fibo.py {arg}
if __name__ == "__main__":
    import sys
    print(sys.path)             # 파이썬 구동 시 환경 변수에 등록되어 있는 디렉터리들의 경로 출력
    print(sys.argv[0])          # 호출된 파일명
    fib(int(sys.argv[1]))       # 첫번째 외부 인자 값을 사용하여 fib 호출
