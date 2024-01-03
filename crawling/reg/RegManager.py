import winreg
import sys


# 레지스트리 값을 읽어오는 클래스
class RegReader:
    _key = winreg.HKEY_LOCAL_MACHINE
    _key_path = "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\"

    def __init__(self):
        fun_name = sys._getframe(0).f_code.co_name

        try:
            self.key = winreg.OpenKeyEx(self._key, self._key_path, 0, access=winreg.KEY_READ)
            print(f"[{fun_name}] 지정된 레지스트리 키를 성공적으로 오픈: {self.key}")
        
        except WindowsError as w_err:
            print(f"[{fun_name}] {w_err}")
            return

    def read_registry_info(self):
        fun_name = sys._getframe(0).f_code.co_name
        query_info_key = winreg.QueryInfoKey(self.key)

        print(f"[{fun_name}] {self._key_path} 아래 {query_info_key[0]}개의 서브 키가 존재합니다.")
        print(f"[{fun_name}] {self._key_path} {query_info_key[1]}개의 값을 포함합니다.")


if __name__ == "__main__":
    rr = RegReader()
    rr.read_registry_info()
    