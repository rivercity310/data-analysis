# [ 사전 타입 ]
# = Map
# 전체 항목이 정렬되지 않은 키와 값의 쌍으로 구성된 집합
# Immutable한 데이터 타입으로 키에 의해 색인이 매겨진다.
# Dict 타입의 Key는 변경이 불가능한 타입이어야 한다. (문자열, 숫자, 튜플 타입 등)

balls = {"red": 4, "blue": 3, "green": 5}
print(f"balls = {balls}, type = {type(balls)}, len = {len(balls)}")

balls["black"] = 1 # 항목 추가
print(balls)

del balls["green"] # 항목 삭제
print(balls)

# 사전의 키들만 추출 -> 일반적으로 list로 변환
print(balls.keys())
print(list(balls.keys()))
print(list(sorted(balls.keys()))) # 사전의 키들을 정렬하여 리스트로 변환

# 사전의 값들만 추출
print(balls.values())
print(list(balls.values()))
print(list(sorted(balls.values()))) # 사전의 값들을 정렬하여 리스트로 변환

# 특정 키 값의 존재 유무 확인
print('blue' in balls)
print('white' not in balls)

# [ dict() ]
# 1. 리스트, 튜플 안의 항목들이 키와 값의 쌍으로 이루어진 튜플인 경우
lst = [('brown', 3), ('gray', 7)]
dt = dict(lst)
print(dt)

tup = (('brown', 3), ('gray', 7))
dt2 = dict(tup)
print(dt2)

# 2. 키가 문자열인 경우 dict 함수의 인자 값 형태로 생성
dt3 = dict(brown=3, gray=7)
print(dt3)

# 사전 타입은 리스트나 튜플같은 열거형 타입보다 속도가 느리다.
# 만약 데이터가 단순히 나열된 숫자로도 충분히 색인이 가능하다면 사전 타입보다는 리스트나 튜플을 사용

# [ comprehension ]
a = {x: x**2 for x in (2, 4, 6)}
print(a)