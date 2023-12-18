import re


# 이메일 주소 정합성 체크
def email_validation_check(email: str) -> bool:
    regex = r"[\w.-]+@[\w.-]+.\w+"

    find_result = re.findall(regex, email)

    if find_result[0] != email:
        print("이메일 주소 형식에 맞지 않습니다 : {}".format(email))
        return False

    print("이메일 주소로 사용 가능합니다! : {}".format(email))
    return True
