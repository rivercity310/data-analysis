# Module: 재사용하고자 하는 변수나 함수의 정의문들을 파일로 저장
# Package: 모듈들을 특정 기준에 따라 모아 놓은 단위

# - import문만 사용한 경우
#       - ex) import sound.effects.echo
#       - sound.effects.echo.echofilter(args)  // 함수 호출을 위해 전체 패키지 및 모듈 경로를 입력해야 함
# - from과 import문을 함께 사용한 경우
#       ex1) from sound.effects import echo
#       - echo.echofilter(args)
#       ex2) from sound.effects.echo import echofilter
#       - echofilter(args)

# from문과 import문이 함께 사용되는 경우 import문 뒤에는 모듈, 서브 패키지, 모듈 내 함수, 클래스, 변수 등이 올 수 있다.
# 반면, import문만 사용하는 경우 마지막 항목이 모듈이나 패키지가 되어야 한다. (클래스나 함수, 변수가 올 수 없음)

# 파이썬 파일 -> 파일명이 곧 모듈명
import fibo

fibo.fib(10)
print(fibo.fib2(20))

# 함수 자체도 객체이므로 변수에 할당 가능
f = fibo.fib
f(30)
print(type(f))      # <class 'function'> : 즉, 함수도 function이라는 클래스에 의해 생성된 객체

# 특정 함수만 import: 이때는 함수명만으로 함수 호출 가능
from fibo import fib
fib(40)

# 모듈을 호출할 때 alias 지정 가능
# import fibo as fb : 모듈에 별칭 지정
from fibo import fib2 as f2
print(f2(30))

# * : 특수한 목적으로 만들어진 함수(언더바(_)로 시작)를 제외한 모든 함수 import
# 함수명 중복이 발생할 우려가 있으므로 모듈을 불러올 때 권장하지 않는 방식 (불러올 함수 명확히 표기)
from fibo import *

# [ import한 모듈 파일이 파이썬 실행 도중 변경된 경우 ]
# importlib 라이브러리의 reload() 함수를 통해 모듈 리로딩
# 기존 imp 라이브러리는 Deprecated
import importlib
importlib.reload(fibo)


# dir() 함수
# - 파이썬 기본 내장 함수로, 모듈 내부를 확인하고 싶을 때 사용
# - 인자로 모듈을 전달할 경우 모듈을 구성하고 있는 변수나 함수의 이름들을 리스트로 반환
# - 아무 인자도 전달하지 않으면 현재까지 파이썬 실행 환경에서 사용하고 있는 변수, 모듈, 함수들의 목록을 리스트로 반환
print(dir(fibo))
print(dir())

# __builtins__ : 파이썬 기본 내장 함수들을 지닌 모듈
import builtins
print(dir(builtins))