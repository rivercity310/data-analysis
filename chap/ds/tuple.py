# [ 튜플 타입 ]
# Immutable한 열거형 타입. 즉, 문자열 타입은 문자로 이루어진 튜플 타입이라고 볼 수 있다.
# 항목을 쉼표로 구분하여 생성하거나 소괄호로 감싸여 선언
movie = 'Superman', 1980, 'Dark Knight', 2010
print(movie)

movie2 = ('Superman', 1980, 'Dark Knight', 2010)
print(movie2)

t = ()
tt = tuple()

# [ vs list ]
# tuple: 서로 다른 종류의 데이터 타입으로 이루어진 항목들을 Unpacking 하거나 색인을 매기는 용도로 사용
# list: 동일한 데이터 타입으로 이루어진 항목들을 순차적으로 다루는 경우 사용

# [ 특징 ]
# 슬라이싱 가능
print(movie[:-2])

# 튜플 내 값 변경 시도
# 1. 튜플 내 객체가 Immutable인 경우 -> TypeError
# 2. 튜플 내 객체가 Mutable인 경우 -> ok
# t2[0] = [4, 5, 6] -> TypeError, 튜플로 감싸져 있기 때문에 안에 있는 리스트 변경 불가
t2 = [1, 2, 3], [4, 5, 6]
t2[0][0] = -1       # 리스트 안에 객체는 변경 가능
print(t2[0][0])

# [ Unpacking ] : 좌측의 변수 개수가 튜플 내 항목 개수와 반드시 일치해야 함
a, b, c, d = movie
print(a, b, c, d)

# [ tuble - list간 형 변환 ]
movie_list = list(movie)  # tuble to list (Immutable to Mutable)
movie_list[1] = 1982      # 리스트는 Mutable이므로 값 변경 가능
print(f"type = {type(movie_list)}, tid = {id(movie)}, lid = {id(movie_list)}")
print(movie_list)

tup = tuple(movie_list)
print(f"type = {type(tup)}, tid = {id(tup)}, lid = {id(movie_list)}")
print(tup)

# [ comprehension ]
tup2 = [(x, x**2) for x in range(6)]
print(tup2)

