# str.format 예제
print('{} is a {}'.format("Chris", "Programmer"))
print('{1} is a {0}'.format("Doctor", "John"))                    # 중괄호 안에 인덱스 지정
print('Good {job}, {name}.'.format(job='PROGRAMMER', name='Chris'))     # 이름 지정 가능

# 언패킹하여 출력 (문자열, 튜플, 리스트 형)
print('{0} - {1} - {2}'.format(*'ABC'))
print('{0} - {1} - {2}'.format(*['A', 'B', 'C']))

# 인덱스 접근을 통한 추출
print('{0[0]} - {0[1]} - {0[2]}'.format(('A', 'B', 'C')))
print('{0[name]} : {0[job]}'.format({'name': 'Seungsu', 'job': 'Programmer'}))

# 출력 정렬
# 콜론 기호(:) - 글자 포맷을 명시하겠다는 의미
# 중괄호 안 숫자 - 출력 결과의 전체 길이 지정
# <, >, ^ - 각각 정렬 방향
# 콜론 기호(:)와 꺾쇠 기호 사이에 특정 문자 - 공백에 해당 문자 채우기
print('{:<20}'.format('좌측 정렬'))
print('{:>20}'.format('우측 정렬'))
print('{:^20}'.format('중앙 정렬'))
print('{:%^20}'.format('중앙 정렬'))        # 중앙 정렬 후 빈칸 % 채우기


import math


print('원주율 크기 {:f}'.format(math.pi))        # f: 소수점 6자리까지 출력 (float)
print('원주율 크기 {:.2f}'.format(3.164))        # .2f: 소수점 둘째짜리까지 출력 (반올림)

print('{:+f} {:+f}'.format(3.14, -3.14))        # +, - 기호 항상 출력
print('{: f} {: f}'.format(3.14, -3.14))        # + 공백, - 기호 출력
print('{:-f} {:-f}'.format(3.14, -3.14))        # - 기호만 출력 (= {:f} {:f})


# 여러 진수로 출력하기
# '#' 접두사를 붙이면 각 진수에 맞는 표준 접두어를 붙여서 출력한다.
# 2진수: 0b, 8진수: 0o, 16진수: 0x

# 포맷 타입
# 2진수(b), 8진수(o), 10진수(d), 16진수(x, X)
print('정수: {0:d}, 16진수: {0:x}, 8진수: {0:o}, 2진수:{0:b}'.format(50))
print('정수: {0:d}, 16진수: {0:#x}, 8진수: {0:#o}, 2진수:{0:#b}'.format(50))

print('{:,d}'.format(10000000))     # 천단위 구분자
print('{:%}'.format(5/12))          # 백분율 사용 (자동으로 100을 곱한 뒤 '%' 기호까지 함께 출력)
print('{:.2%}'.format(5/12))        # 백분율에 소수점 제약


# [ printf-style 문자열 포맷 ]
# 더이상 사용하지 않음 (권고 X) - 가급적이면 str.format() 형식 사용
# 튜플이나 사전 타입 데이터를 제대로 출력하지 못하는 문제점
print("The value of PI is approximately %5.3f" % math.pi)


# [ f-string ]
# Python 3.6에 등장
# 로깅의 문자열이 아직 f-string을 지원하지 않기 때문에 str.format() 사용
print(f"The value of PI is approximately {math.pi:5.3f}")
