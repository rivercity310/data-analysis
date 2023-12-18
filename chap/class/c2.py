# [ __init__() 재정의 ]
# constructor 역할
# self.name = name: 객체 인스턴스 생성시 해당 인스턴스에 속한 name이라는 변수(인스턴스 변수)를 생성하겠다는 의미
class BookReader2:
    def __init__(self, name):
        self.name = name

    def read_book(self):
        print(f"{self.name} is reading book!!")


reader = BookReader2("Chris")
reader.read_book()
del reader


# [ 클래스 변수와 인스턴스 변수 ]
class BookReader3:
    country = "South Korea"  # Java의 static 변수와 같은 개념

    def __init__(self, name):
        self.name = name  # 인스턴스 변수 name

    def read_book(self):
        print(f"{self.name} is reading book in {self.country}")


reader = BookReader3("Seungsu")
reader.read_book()

# [ 클래스 변수에 Immutable한 데이터 타입을 쓰는 경우 ]: 공유 안됨
# 객체 1에서 클래스 변수 변경 -> Immutable이므로 새로운 객체 생성 -> 객체 2에서 접근 불가
# 즉, 클래스 변수는 인스턴스화를 하는 시점에 객체에 내려받는다.
reader2 = BookReader3("Heejung")
reader2.country = "USA"
print(reader.country)  # South Korea
print(reader2.country)  # USA
del reader, reader2


# [ 클래스 변수에 Mutable한 데이터 타입을 쓰는 경우 ]
# 공유 됨(주의): 공유를 의도한 것이 아니라면, 인스턴스 변수를 사용해야 함
class Dog:
    tricks = []

    def __init__(self, name):
        self.name = name

    def add_trick(self, trick):
        self.tricks.append(trick)


fido = Dog("Fido")
buddy = Dog("Buddy")

fido.add_trick("구르기")
buddy.add_trick("두 발로 서기")

print(fido.tricks)  # '구르기'와 '두 발로 서기'가 둘 다 들어가 있음
