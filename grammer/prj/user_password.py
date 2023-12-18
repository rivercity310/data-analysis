import re


# 비밀번호 정합성 체크를 위한 함수 (정규식을 사용하지 않은 버전)
def password_validation_check(pwd: str) -> bool:
    """ checking password validation

    :param pwd: password string

    :return: True or False (the result of checking)
    """
    # 비밀번호 길이 확인 (6 ~ 12)
    if len(pwd) < 6 or len(pwd) > 12:
        print(pwd, "의 길이가 적당하지 않습니다.")
        return False

    # 숫자 혹은 알파벳 유무 확인
    for c in pwd:
        if not c.isnumeric() and not c.isalpha():
            print(pwd, "은(는) 숫자와 영문자로만 구성되지 않았습니다.")
            return False

    # 대소문자 확인
    upper = False
    lower = False

    for c in pwd:
        # 대문자, 소문자가 모두 존재하는 경우 루프 탈출
        if upper and lower:
            break

        # 해당 문자가 영문이면
        if c.isalpha():
            # 아직 대문자가 발견되지 않은 경우
            if not upper:
                upper = c.isupper()

            # 아직 소문자가 발견되지 않은 경우
            if not lower:
                lower = c.islower()

    # 대문자 혹은 소문자가 모두 존재하는지 확인
    if not upper or not lower:
        print(pwd, "은(는) 영문 대문자와 소문자가 함께 존재하지 않습니다.")
        return False

    print(pwd, "은(는) 비밀번호로 적당합니다!")
    return True


def password_validation_check_re(pwd: str) -> bool:
    """ checking password validation using reg expression

    :param pwd: (str) password string

    :return: True or False (the result of checking validation
    """
    if len(pwd) < 6 or len(pwd) > 12:
        print(pwd, "의 길이가 적당하지 않습니다.")
        return False

    # 숫자 혹은 알파벳 유무 확인
    if re.findall('[a-zA-Z0-9]+', pwd)[0] != pwd:
        print(pwd, "은(는) 숫자와 영문자로만 구성되지 않았습니다.")
        return False

    # 알파벳 대소문자 확인
    if len(re.findall('[a-z]', pwd)) == 0 or len(re.findall('[A-Z]', pwd)) == 0:
        print(pwd, "은(는) 영문 대문자와 소문자가 함께 존재하지 않습니다.")
        return False

    print(pwd, "은(는) 비밀번호로 적당합니다!")
    return True


if __name__ == "__main__":
    password_validation_check("23jke")
    password_validation_check("23jke213")
    password_validation_check("23jke2A13")
    password_validation_check("290$#asdkqw")

    password_validation_check_re("23jke")
    password_validation_check_re("23jke213")
    password_validation_check_re("23jke2A13")
    password_validation_check_re("290$#asdkqw")

