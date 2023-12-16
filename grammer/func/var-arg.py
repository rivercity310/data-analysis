# [ 여러 개 인자 값 및 키워드 인자 ]
# 필수 인자 값: 함수 호출 시 반드시 값을 대입해야 하는 인자
# 옵션 인자 값: 값을 대입하지 않은 경우 기본 값 할당
# 위치 인자 값: 인자 값을 집어 넣는 순서가 중요한 필수 인자 값
# 키워드 인자 값: 기본 값을 가지고 있는 옵션 인자 값
def introduce_my_car(manufacturer, seats=4, type='sedan'):
    print(f"내 차는 {manufacturer}의 {seats}인승 {type}이다.")


introduce_my_car('현대')
introduce_my_car(manufacturer='기아')
introduce_my_car(type='SUV', manufacturer='BMW')


# 주의 사항
# 키워드 인자 값 뒤에 키워드 없는 인자 값 사용 불가 -> SyntaxError
# introduce_my_car(manufacturer='현대', 2)

# [ 가변 인자 리스트 활용 ] : 열거된 매개변수 -> 함수 인자 값 패킹
# * : 튜플 타입
# ** : 사전 타입
# var-positional: 나열한 값들이 알아서 각 변수에 패킹되어 대입됨
def introduce_family(name, *family_names, **family_info):
    print("제 이름은 {}입니다.".format(name))
    print("제 가족들의 이름은...")

    for family_name in family_names:
        print(family_name)

    print("-" * 40)

    for key in family_info.keys():
        print("{}: {}".format(key, family_info[key]))


introduce_family('Chris', 'Jihee', 'Anna', 'Shinhoo', 집='용인', 가훈='행복하게 살자')


# 가변 인자 값을 앞쪽에 배치하고 뒤에 인자 값이 위치하는 경우에는
# 뒤쪽에 배치된 일반 인자 값은 반드시 키워드 인자 값 형태로 사용 -> Keyword-only
def concat(*args, sep="/"):
    return sep.join(args)


print(concat("earth", "mars", "venus"))
print(concat("earth", "mars", "venus", sep=","))

# [ 언패킹 인자 리스트 활용 ] : 열거형 데이터 -> 함수 인자로 언패킹
# * : 튜플 타입 언패킹
# ** : 사전 타입 언패킹
args1 = [3, 6]
args1_tup = (3, 6)
print(list(range(*args1)))
print(list(range(*args1_tup)))

args2 = {'manufacturer': '현대', 'seats': 9, 'type': 'SUV'}
introduce_my_car(**args2)