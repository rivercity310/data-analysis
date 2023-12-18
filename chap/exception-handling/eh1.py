import traceback


# 1. 일반적인 예외 처리
def exception_test():
    print("[1] Can add 2 + '2' in Python?")

    try:
        print("[2] Trying.. : {}".format(2 + '2'))
    except TypeError as err:        # TypeError가 발생하면 해당 인스턴스를 err 변수에 할당
        print("[2] TypeError Catch : {}".format(err))
        traceback.print_exc()       # traceback 메세지 출력
        raise NameError
    except (NameError, ArithmeticError) as err:    # 여러 예외 처리
        print(err)
        pass
    except:                                 # 모든 예외 처리 (사용X)
        # 로깅
        # 해당 에러 재발생 raise
        raise
    finally:
        print("finally")


# 2. except-else-finally
# 예외가 발생하면 except, 아니면 else
def exception_test2(file_name: str):
    f = None

    try:
        f = open(file_name, "r", encoding="UTF-8")
    except IOError:
        print("cannot open file {}".format(file_name))
    else:
        print("file has {} lines".format(len(f.readlines())))   # f 변수를 여기서 사용 가능
        f.seek(0, 0)        # cursor 첫번째로 이동
        print("".join(f.readlines()))
    finally:
        print("tried to read file {}".format(file_name))
        if not f.closed:
            print("closed file.. {}".format(file_name))
            f.close()


# 3. 사용자 정의 예외와 raise
# Exception 클래스를 상속받는 예외 클래스 정의
class TooBigNumError(Exception):
    def __init__(self, val: int) -> None:    # 초기화 메서드 재정의
        self.val = val

    def __str__(self) -> str:          # 에러 메세지 함수 재정의
        return "Too Big Number {}. Use 1 ~ 10!".format(self.val)


def exception_test3():
    num = int(input("정수 입력: "))

    if num > 10:
        raise TooBigNumError(num)

    print("숫자 {} 입력!".format(num))


if __name__ == "__main__":
    # exception_test()
    # exception_test2("../logging/python.log")
    # exception_test2("../logging/python2.log")
    exception_test3()
