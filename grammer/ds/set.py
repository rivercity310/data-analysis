# [ 세트 타입 ]
# 색인에 의한 순서가 없고, 중복이 허용되지 않는 데이터들의 집합
# 항목들을 중괄호로 감싸서 선언
lang = {"Java", "Python", "Java", "C++"}
print(lang)
print("Java" in lang)

# 빈 set 타입은 반드시 set() 함수로만 가능 -> Dict와 중복되기 때문
# s1 = {} 불가능
s1 = set()

# [ 집합 연산 ]
a = set('abracadabra')
b = set('alacazam')

print(a)
print(b)

print(a - b) # 차집합
print(a | b) # 합집합
print(a & b) # 교집합
print(a ^ b) # 여집합 = (a - b) | (b - a)
print((a - b) | (b - a))

# [ comprehension ]
a = {x for x in 'abracadabra' if x not in 'abc'}
print(a)