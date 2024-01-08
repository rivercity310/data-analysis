import openpyxl


class ExcelManager:
    _excel_file_path = r"C:\Users\seungsu\Desktop\employment\지원이력.xlsx"

    def __init__(self):
        self.excel_file = openpyxl.load_workbook(self._excel_file_path, data_only = True)

    
    def get_excel_data(self, row, col: str):
        sheet = self.excel_file["Sheet1"]
        return sheet.cell(row, self.col_to_int(col)).value


    def set_excel_data(self, row, col: str, val):
        sheet = self.excel_file["Sheet1"]    
        sheet.cell(row, self.col_to_int(col), val)
        self.excel_file.save(self._excel_file_path)


    def col_to_int(self, col: str) -> int:
        val = ord(col) - ord('A') if col.isupper() else ord(col) - ord('a')
        return val + 1
    

if __name__ == "__main__":
    em = ExcelManager()
    