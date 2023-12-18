# [ Logging ]
# - 소프트웨어에서 일어나는 이벤트들을 추적하기 위한 용도
# - 일반적으로 별도의 파일에 저장되어 체계적으로 관리됨

# [ Log Level ]
# 5개로 구분, 중요도가 높아지는 순서
# - DEBUG: 상세한 정보, 문제를 분석할 때 필요한 로그
# - INFO: 소스 코드가 기대대로 동작하는지 확인하기 위한 로그
# - WARNING: 소프트웨어는 잘 동작하고 있는 상황이지만, 추후 일어날 위험을 알려주기 위한 로그
# - ERROR: 소프트웨어의 일부 기능이 제대로 동작하지 않을 때 필요한 로그
# - CRITICAL: 소프트웨어가 더 이상 실행할 수 없을 때 필요한 로그

# 로그 레벨이 WARNING -> DEBUG, INFO 출력 x, 그 이상 단계의 로그만 출력됨

import logging

logging.warning("조심하세요!")        # WARNING 메세지 출력
logging.info("정보 확인하세요!")       # INFO 메세지 출력되지 않음

# {log-level}:{default-logger}:{msg} 순으로 로그가 출력됨
# 기본 로거(default-logger): 로깅을 하는 주체로, 기본적으로 'root'로 지정되어 있음.
# Python의 기본 로거인 root의 로그 레벨이 WARNING이므로 INFO와 DEBUG 레벨의 로그는 출력되지 않는다.
logging.root.setLevel(logging.DEBUG)    # 로그 레벨 변경
logging.info("정보 확인하세요!")           # INFO 메세지 출력 됨


# [ print() 로깅 ]
# - 개발 환경의 소스 코드를 운영 환경으로 내보낼 때 번거로워짐
# - Side-Effect 발생 위험
# 따라서 각각의 레벨에 맞는 로그를 작성하여 환경 별 다른 로그를 제공 (운영자, 개발자, 사용자)
# - 운영자: ERROR 로그 레벨로 에러 내용만 확인, 필요시 로그 레벨을 하향하여 추가 로그 얻을 수 있음
# - 개발자: DEBUG 로그 레벨로 전체 로그 확인
# - 사용자: 로그를 볼 필요가 없음


# [ 로깅 모듈 구성 ]
# 1. Loggers
#   - 로깅을 하는 주체
#   - 로깅 인터페이스 제공
#   - 최상단 root 로거 밑으로 모듈 단위로 로거가 생성됨. (부모-자식 관계)
#   - 여러 개의 핸들러를 보유할 수 있음.
# 2. Handlers
#   - 로거에 의해 생성된 로그 레코드를 적절한 곳에 출력한다. (콘솔, 파일, DB 등)
#   - 특정 로거 객체에 귀속됨
# 3. Formatters
#   - 로그의 출력 포맷 결정
# 4. Log Record
#   - 로그 한 줄이 생길 때마다 생성되는 객체
#   - 로거 이름, 로그 레벨, 로그를 발생시킨 소스 코드 위치 등의 정보를 담고 있음

# [ logger ]
# 자체적으로 인스턴스를 생성할 수 없고, logging.getLogger()를 통해 인스턴스를 얻는다.
# 인자 값(로거 이름)으로 어떠한 문자열을 집어 넣어도 상관 없으나, 모듈 단위로 생성하는 것이 좋음
logger = logging.getLogger(__name__)        # __name__ : 모듈의 이름을 담고 있는 변수
logger.warning("곧 문제가 생길 가능성이 높습니다.")

# formatter 생성
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)8s - %(message)s')

# 핸들러에 포매터 설정
# 콘솔(StreamHandler), 파일(FileHandler)
handler = logging.StreamHandler()     # 콘솔 출력용 핸들러 생성
handler.setFormatter(formatter)

# 로그 레벨 설정, 핸들러 추가
logger.setLevel(logging.INFO)
logger.addHandler(handler)

# 로그 메세지 출력
logger.debug("이 메시지는 개발자용입니다.")
logger.info("생각대로 동작하네요.")
logger.warning("곧 문제가 생길 가능성이 있어요.")
logger.error("특정 기능이 동작하지 않습니다.")
logger.critical("시스템이 다운되었습니다.")

# [ log record의 속성명 ]
# 위 formatter 내 소괄호에 지정된 로그 레코드의 속성명
# s(문자열), d(정수), f(실수)
"""
asctime     %(asctime)s     로그 레코드 생성 시간
filename    %(filename)s    로깅 소스 코드가 작성된 파일 이름 (확장자 포함)
funcName    %(funcName)s    로깅을 호출한 함수 이름
levelname   %(levelname)s   로그 레벨
lineno      %(lineno)d      로그 소스 코드의 줄 위치
module      %(module)s      모듈 이름 (확장자 미포함)
message     %(message)s     로깅 메세지
name        %(name)s        로거 이름
pathname    %(pathname)s    로깅 소스 코드가 작성된 파일의 절대 경로
"""

# [ 로그 레벨 ]
# 로그 레벨은 로거나 핸들러 등에 모두 설정이 가능.
# 상위 객체에 설정된 로그 레벨에 의해 한차례 걸러져서 하위 객체로 전달됨
# ex1) root의 로그레벨이 WARNING: 하위 로거 객체는 WARNING 이상만 출력
# ex2) handler의 로그레벨이 INFO, Logger의 로그 레벨이 WARNING: WARNING 이상만 출력
# 즉, root 로거로부터 계층 구조에 따라 아래로 내려갈 수록 로그 레벨을 점점 더 높아질 수 밖에 없다. (필터링)

# [ 로그 레벨 설정 ]
# 1. root 로거의 로그 레벨을 DEBUG 또는 NOTSET으로 세팅 (모든 로그 출력)
# 2. 로그 레벨을 제어하고 싶은 단위로 로거 생성(모듈 또는 패키지 단위)
# 3. 생성된 하위 로거에 로그 레벨 지정
# 4. 핸들러에는 따로 로그 레벨을 지정 x, 속한 로거를 따라가게 함 (여러 로거에 속할 수 있기 때문)
# *핸들러의 기본 로그 레벨: NOTSET
