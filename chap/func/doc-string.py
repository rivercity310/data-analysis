# [ documentation strings ]
# 세 개의 쌍 따옴표 안에 함수에 대한 설명을 기술한다.
# 함수의 docstring을 출력하려면 '__doc__' 내장 변수를 호출한다.
def doc_func(arg1: int = 0, arg2: int = 1) -> int:
    """함수의 간단한 설명을 기술하는 부분.

    각 매개변수에 대한 설명을 적는 부분.
    :param arg1: (int) the first argument (default = 0)
    :param arg2: (int) the second argument (default = 1)

    :return: (int) arg1 + arg2
    """
    return arg1 + arg2


print(doc_func.__doc__)