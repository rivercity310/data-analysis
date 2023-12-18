# user 관련 모듈 탑재
import user_email as ue
import user_password as up


# 사용자 클래스 정의
class User:
    """ class for user management

    Put email address & password when creating instance.
    And also need to check validation of address & password.
    """
    # 초기화 함수 재정의
    def __init__(self, email: str, pwd: str):
        self.email = email
        self.pwd = pwd
        self.check_validation()

    # 정합성 검증 함수
    def check_validation(self):
        ue.email_validation_check(self.email)
        up.password_validation_check_re(self.pwd)


if __name__ == "__main__":
    user1 = User("isi.cho@gmail.com", "3jkMf8Exe")
    user2 = User("isi.cho@gmail^c@m", "eee")
