import re


# 이메일 주소 정합성 체크
def email_validation_check(email: str) -> bool:
    """ checking email address validation

    :param email: (str) email address

    :return: True or False (the result of checking validation)
    """
    # r: 앞으로 나올 문자열을 파이썬 문자열 특수 기호로 인식하지 않고 raw 포멧으로 인식하겠다는 의미
    if re.findall(r'[\w.-]+@[\w.-]+.\w+', email)[0] != email:
        print(email, "은(는) 이메일 주소 형식에 맞지 않습니다.")
        return False

    print(email, "은(는) 이메일 주소로 적당합니다!")
    return True


if __name__ == "__main__":
    email_validation_check("#@c#0@gmail*om")     # False
    email_validation_check("isi.cho@gmail.com")  # True
