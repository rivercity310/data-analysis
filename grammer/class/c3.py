# [ 데이터 은닉(캡슐화) ]
# Python에서는 접근 제한자를 제공하지 않음
# 따라서 이름 장식(Name Mangling) 기법을 통해 캡슐화 구현: 클래스 변수 앞에 언더바 두개
# 이름 장식: 기존 변수명으로 클래스 변수를 확인할 수 없도록 클래스 변수명을 변경해버림 (규칙: _[클래스명]__[변수명])
# 물론, 위 규칙을 통해 바로 접근할 수는 있지만 의도치 않은 변경을 막을 수는 있음

# 캡슐화된 클래스 변수는 메서드를 통해 수정
class BookReader:
    __country = "South Korea"     # 이름 장식을 통해 '_BookReader__country'로 변경됨

    def update_country(self, country):
        self.__country = country

    def get_country(self):
        return self.__country


print(dir(BookReader))
reader = BookReader()
reader.update_country("USA")
print(reader.get_country())
print(reader._BookReader__country)      # 접근 가능
print(BookReader.__sizeof__(reader))    # 32Byte


# [ Inheritance ]
class Human:
    __country = "South Korea"

    def __init__(self, name):
        self.name = name

    def update_country(self, country):
        self.__country = country

    def get_country(self):
        return self.__country

    def eat_meal(self):
        print(f"{self.name} is eating meal!!")


class Singer(Human):
    def sing(self):
        print(f"{self.name} is singing in {self.get_country()}")


class Drummer(Human):
    def play_drum(self):
        print(f"{self.name} is playing drum in {self.get_country()}")


# __init__ 함수도 부모 클래스(베이스 클래스)로부터 상속된다.
singer = Singer("Seungsu")
singer.sing()
singer.eat_meal()

drummer = Drummer("Heejung")
drummer.play_drum()
drummer.eat_meal()

print(singer.__class__)     # singer 인스턴스의 타입 (Singer 클래스)
print(Singer.__class__)     # Singer 클래스의 타입 (type 클래스)
print(Singer.__bases__)     # Singer 클래스의 부모 클래스(베이스 클래스)
print(Human.__class__)      # Human 클래스의 타입 (type 클래스)
print(Human.__bases__)      # Human 클래스의 부모 클래스 (object 클래스: 상속 계층 구조의 가장 높은 곳에 위치한 클래스)


# [ 다중 상속 ]
# bases 복수형인 이유: 부모 클래스가 한 개가 아닌 여러 개가 될 수도 있음을 암시
class Developer:
    def coding(self):
        print(f"{self.name} is developer!!")


class ProgramBookWriter(Human, Developer):
    def write_book(self):
        print(f"{self.name} is writing book!!")


pbw = ProgramBookWriter("Chris")
pbw.eat_meal()
pbw.coding()
pbw.write_book()
print(ProgramBookWriter.__bases__)