# [ 설정 파일을 활용한 로깅 ]
# logging.conf
# 소스 코드 상에서 로그 레벨을 지정하게 되면 수정이 번거로움
# 따라서 별개의 설정 파일에 로깅 설정 내용을 저장해두고 소스 코드에서는 해당 파일을 읽어 사용한다.

import logging
import logging.config   # 로깅 설정 모듈

# 설정 파일 읽어오기
logging.config.fileConfig("./logging.conf")

# 로거 생성
logger = logging.getLogger(__name__)

# 로그 메세지 출력
logger.debug("이 메시지는 개발자용입니다.")
logger.info("생각대로 동작하네요.")
logger.warning("곧 문제가 생길 가능성이 있어요.")
logger.error("특정 기능이 동작하지 않습니다.")
logger.critical("시스템이 다운되었습니다.")
