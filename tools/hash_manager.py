# 작성자: 황승수
# 작성일: 2024/01/04
# 소속: AhnLab EPI 개발팀 PatchLab
# 직급: 인턴


import os
import hashlib


class HashManager:
    # 이 경로 하위에 있는 모든 폴더를 탐색하여 파일을 찾습니다.
    # 해당 파일의 파일명, MD5, SHA256, 파일크기를 추출하고
    # _default_path 경로에 hash.txt 파일을 생성하여 추출 정보를 기록합니다.
    # 혹은 self.text_file_path를 수정하여 원하는 위치에 hash.txt 파일을 저장할 수 있습니다.

    _default_path = "C:\\Program Files\\Git"

    def __init__(self):
        self.file_dir_list = os.listdir(self._default_path)
        self.file_path_list = list()
        self.hash_result_list = list()
        self.text_file_path = self._default_path + "\\" + "hash.txt"

        if os.path.exists(self.text_file_path):
            print("기존 hash.txt 파일을 삭제합니다...")
            os.remove(self.text_file_path)

    
    def start(self, path = _default_path):
        if os.path.isfile(path) or path.endswith(".msp"):
            dir, file = os.path.split(path)
            self.file_path_list.append((dir, file))
            print(f"\t파일 발견: {path}")
            return
        
        # 폴더면 한 뎁스 더 들어간다
        list_dir = os.listdir(path)

        for f in list_dir:
            print(f"현재 경로: {path}")
            self.start(path + "\\" + f)

    
    def load_hash_value(self):
        for dir, file in self.file_path_list:
            print(f"[작업 중...] dir: {dir}, file: {file}")
            file_path = dir + "\\" + file

            with open(file_path, "rb") as fp:
                binary = fp.read()
                md5 = hashlib.md5(binary).hexdigest()
                sha256 = hashlib.sha256(binary).hexdigest()

            self.hash_result_list.append((dir, file, md5, sha256))
        
        del self.file_path_list
        print("모든 파일에 대한 해시 정보 추출이 완료되었습니다.")

    
    def write_result_on_text_file(self):
        for dir, file, md5, sha256 in self.hash_result_list:
            tmp = ""
            file_size = os.path.getsize(dir + "\\" + file)

            tmp += "----------------------------------\n"
            tmp += f"파일명: {file}\n"
            tmp += f"파일 크기: {file_size / (1000 ** 2): .2f}MB\n"
            tmp += f"md5: {md5}\n"
            tmp += f"sha256: {sha256}\n"
            tmp += "----------------------------------\n\n"

            with open(self.text_file_path, "at", encoding="utf8") as fp:
                fp.write(tmp)


if __name__ == "__main__":
    hm = HashManager()
    hm.start()
    hm.load_hash_value()
    hm.write_result_on_text_file()        