import openpyxl
import os
import datetime


class ExcelManager:
    # 엑셀 파일 경로
    _original_file_path = r"D:\patch.xlsx"
    _sheet_name = "dotnet"

    def __init__(self):
        if not os.path.exists(self._original_file_path):
            print("원본 파일이 존재하지 않습니다.")
            print("프로그램을 종료합니다...")
            return

        default_dir = "D:\patch"

        if not os.path.exists(default_dir):
            print("복사 파일이 저장될 폴더를 만듭니다.")
            os.mkdir(default_dir)

        now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        self.excel_file_path = default_dir + "\\patch" + now + ".xlsx"

        with open(self._original_file_path, "rb") as fp:
            with open(self.excel_file_path, "wb") as fp2:
                fp2.write(fp.read())

        self.excel_file = openpyxl.load_workbook(self.excel_file_path, data_only = True)
        print(self.excel_file)
    
    
    def _col_to_int(self, col: str) -> int:
        val = ord(col) - ord('A') if col.isupper() else ord(col) - ord('a')
        return val + 1
    


if __name__ == "__main__":
    em = ExcelManager()
