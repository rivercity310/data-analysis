from hash_manager import HashManager
from datetime import datetime



class DotnetHashManager(HashManager):
    # 탐색하고자 하는 파일/폴더의 이름 (startswith 조건)
    _include_folders_name = []
    _include_files_name = ["windows"]

    def __init__(self):
        super().__init__(self._include_files_name)
        self.hash_result_list = super().get_hash_result()
        print(self.hash_result_list)


    def _get_dict_once_probs(self, qnumber: str):
        return {
            "Bulletine ID": f"MS-KB{qnumber}",
            "KBNumber": f"KB{qnumber}",
            "PatchDate": datetime.today().strftime("%Y/%m/%d"),
            "중요도": "TMP 중요도",
            "cve": "TMP cve"
        }
    
    
    def _get_dict_multiple_probs(self, file, file_size, md5, sha256):
        return {
            "Title": "TMP title",
            "Summary": "TMP Summary",
            "BulletinUrl": "TMP BulletinUrl",
            "파일명": file,
            "파일크기": f"{file_size / (10 ** 6):.2f}",
            "MD5": md5,
            "SHA256": sha256,
            "Wsus 파일": "TMP WSUS 파일"
        }
    

if __name__ == "__main__":
    dhm = DotnetHashManager()