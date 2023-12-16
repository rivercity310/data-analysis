# [ documentation strings ]
# 세 개의 쌍 따옴표 안에 함수에 대한 설명을 기술한다.
# 함수의 docstring을 출력하려면 '__doc__' 내장 변수를 호출한다.
def doc_func(arg1=0, arg2=1):
    """함수의 간단한 설명을 기술하는 부분.

    각 매개변수에 대한 설명을 적는 부분.
    arg1: the first argument (default = 0)
    arg2: the second argument (default = 1)
    """
    pass


print(doc_func.__doc__)