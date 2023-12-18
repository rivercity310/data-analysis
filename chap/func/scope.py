# [ 함수 내 변수의 유효 범위 ]
# Scope: 변수를 사용할 때 해당 변수가 영향을 미치는 영역

# Test 1.
# 이 경우에는 전역변수 param의 값을 변경하는 것이 아닌, 함수 내에서 param이라는 지역 변수를 새로 생성한다. (객체 식별자 값이 다름)
# 즉, Immutable 데이터 타입인 문자열 변수의 값을 변경하려고 하니 새로운 객체가 생성되었고,
# 함수 내에서만 사용할 수 있는 객체(지역 변수)가 param 변수에 대입된 것
def test_func():
    param = "Modified by test_func"
    print("param = {}, id = {}".format(param, id(param)))


param = "Create from Outside"
test_func()
print("param = {}, id = {}".format(param, id(param)))

del param  # 기존 param 변수 삭제


# Test 2.
# 이 경우에는 전역변수 param을 함수 내부에서 출력하고 있다. (동일한 객체 식별자 값)
def test_func2():
    print("param = {}, id = {}".format(param, id(param)))


param = "Create from Outside"
test_func2()
print("param = {}, id = {}".format(param, id(param)))
del param


# Test 3.
# 다음 함수는 UnBoundLocalError를 일으킨다.
# 파이썬에서는 함수 내에서 어떤 변수에 값을 할당하는 경우, 할당하는 위치와 상관 없이 무조건 지역 변수로 인식한다.
# 즉 test_func3의 첫번째 라인에서 param 변수를 아직 생성하지 않은 지역 변수라고 인식하는 것. (다른 언어와의 차이점)
def test_func3():
    print(param)  # UnBoundLocalError
    param = "Modified by test_func3"
    print(id(param))


param = "Create from Outside"

try:
    test_func3()
except UnboundLocalError as err:
    print("error")
finally:
    print("param = {}, id = {}".format(param, id(param)))
    del param


# Test 4.
# 함수 내에서 호출한 param 변수가 전역 변수임을 알려주는 키워드 global을 사용
def test_func4():
    global param
    param = "Modified by test_func4"  # 여기서 객체 식별자 값 변경됨
    print("param = {}, id = {}".format(param, id(param)))


param = "Create from Outside"
print("param = {}, id = {}".format(param, id(param)))
test_func4()
print("param = {}, id = {}".format(param, id(param)))


# 함수 중첩 시 변수 Scope 구분
# 외부 함수와 내부 함수 사이에서 생겨나는 nonlocal/enclosing 범위
# outer(), inner() 입장에서 전역(global) 범위
def outer():
    # outer() 입장에서 지역(local) 범위
    # inner() 입장에서 비지역(nonlocal) 범위
    num = 0     # inner() 함수 입장에서 비지역 변수 num

    def inner():
        # inner() 입장에서 지역(local) 범위
        nonlocal num
        num = 3
        print("[inner()] num = {}, id = {}".format(num, id(num)))

    inner()
    print("[outer()] num = {}, id = {}".format(num, id(num)))


outer()

# 위 경우에서 nonlocal 키워드를 주석 처리하면 inner() 함수에서 새로운 num 변수를 생성한다.
# 따라서 각각의 num이 0과 3을 출력하고, 다른 객체 식별자 값을 가진다.

# 하지만 nonlocal 키워드를 추가하면 inner() 함수 내에서 새로운 변수 생성을 막고 비지역 범위에 있는 num 변수를 활용한다.
# 따라서 두 함수가 똑같이 3을 출력하고, 같은 객체 식별자 값을 가진다.
