# [ 리스트 타입 ]
# - 여러 값을 동일한 변수에 순차적으로 저장할 수 있는 용도
# - 값을 변경할 수 있는 Mutable 데이터 타입: 내장 메서드 id() 함수를 통해 객체 식별자 확인
# - Immutable: 새 값 할당 시 객체 식별자 변경, Mutable: 새 값을 할당 시 객체 식별자 유지 (기존 값 대체)

# [ 빈 리스트 생성 ]
# 1. empty_list = []
# 2. empty_list = list()

# [ 리스트 타입 함수 ]
# append() : 리스트 끝에 값 추가
# remove(val) : 리스트 내 특정 값 삭제
# insert(idx, val) : idx 위치에 val 삽입
# pop(idx) : idx 위치의 값을 제거하고 해당 값 반환, idx를 주지 않으면 마지막 위치 값 제거 후 반환

# [ 리스트 슬라이싱 ]
# 변수명[start:end] : 리스트 타입 변수의 start 색인부터 end-1 색인까지 슬라이싱
# shallow copy : 리스트 변수를 다른 변수에 그대로 할당 -> 객체 식별자 값 공유, 한 변수의 값 변경 시 다른 변수에도 영향을 미침
# deep copy : pockets_copy = pockets[:] -> 서로 다른 객체 식별자 값, 메모리 상에서 독립적으로 존재
lst = [5]
shallow_copy = lst
shallow_copy.append(3)
print(lst)  # [ 5, 3 ]
print(id(lst) == id(shallow_copy))

deep_copy = lst[:]
deep_copy.append(6)
print(lst)  # lst = [ 5, 3 ]
print(deep_copy)  # hard_copy = [ 5, 3, 6 ]
print(id(lst) == id(deep_copy))

# [ 리스트 타입 데이터 합치기 & 확장하기 ]
# 1. 두 리스트를 '+' 연산을 통해 합치는 경우 (a = b + c) : a, b, c 각각의 객체 식별자가 모두 다름 (Deep Copy)
# 2. a.extend(b) : 객체를 새로 생성하지 않고 a에 b 리스트 항목 추가 -> c를 생성하지 않기 때문에 메모리를 효율적으로 사용

# [ 리스트 삭제 del ]
# - pop과의 차이점은 해당 색인의 값을 반환하지 않고 인자 값으로 리스트의 일부분을 줄 수 있다는 점
# del a[0] : 리스트 첫번째 값 삭제
# del a[1:3] : 리스트 부분 삭제
# del a[:] : 리스트 전체 값 삭제 (빈 리스트 만들기)
# del a : 변수 자체 삭제, 이후 호출 불가

# [ 예외 ]
# 리스트 타입 자체는 Mutable 데이터 타입이지만 Immutable 데이터 타입인 문자열에 의해 자동으로 생긴 리스트는 값을 마음대로 변경할 수 없다.
word = "파이썬 문자열 색인"
print(id(word), end="\n")

try:
    word[-2:] = "추출"
except TypeError:
    print("예외 발생")

# word[-2:] = "추출" -> 문자열 타입은 값을 변경할 수 없기 때문에 TypeError 발생
# 아래처럼 새로운 객체를 생성하여 원하는 문자열을 만들어야 한다. (새로운 객체 식별자 값이 할당됨)
word = word[:-2] + "추출"
print(id(word), end="\n")

# range 타입을 이용하여 순차적인 값을 가지는 리스트 생성 가능
a = list(range(10))
print(a)

# list comprehension
# - 리스트 외 다른 자료구조에서도 사용 가능
b = [x for x in range(10)]
print(b)

A = ['blue', 'green', 'red']
B = ['red', 'green', 'blue']
pairs = [(a, b) for a in A for b in B if a != b]
print(pairs)
