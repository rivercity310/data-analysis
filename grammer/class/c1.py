# [ 파이썬은 모든 것이 객체 ]
# 클래스 역시 객체이므로 str 클래스도 type이라는 클래스의 객체이다.
var = "Python"
print(f"type = {type(var)}, id = {id(var)}")
print(f"type = {type(str)}, str = {str}, id = {id(str)}")
print(f"class = {var.__class__}, replace = {var.replace('Python', '파이썬')}")


# [ 클래스 정의 ]
# self: 자신의 객체를 인자 값으로 넘김으로써 함수 내에서 클래스의 속성 및 메서드에 접근할 수 있게 함
# 메서드 내에서도 self.속성명 형태로 클래스의 속성에 접근해야 함
class BookReader:
    name = str()

    def read_book(self):
        print(f"{self.name} is reading book!!")

    class Reader:
        nme = str()

        def read(self):
            print(f"{self.nme} : hi")


# __main__: 현재 클래스가 생성된 위치를 나타냄 (파이썬 실행의 최상단 레벨의 코드에서 실행되었다는 의미)
# __main__에 속한 클래스는 전역에서 호출이 가능하다.
reader = BookReader()
print(type(reader))     # <class '__main__.BookReader'>
reader.name = 'Chris'
reader.read_book()
