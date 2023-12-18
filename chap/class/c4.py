# [ Polymorphism ]
class Developer:
    def __init__(self, name):
        self.name = name

    def coding(self):
        print(f"{self.name} is coding")


class JavaDeveloper(Developer):
    # overriding
    def coding(self):
        print(f"{self.name} is Java Coding")


class PythonDeveloper(Developer):
    def __init__(self, name):
        super().__init__(name)

    # overriding
    def coding(self):
        super().coding()        # super(): 부모 클래스의 인스턴스가 호출되어 부모 클래스의 속성이나 메서드 호출 가능
        print(f"{self.name} is Python Coding")


dv = Developer("d1")
dv.coding()

jd = JavaDeveloper("d2")
jd.coding()

pd = PythonDeveloper("d3")
pd.coding()