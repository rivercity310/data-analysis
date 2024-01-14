from crawling_manager import CrawlingManager
from bs4 import BeautifulSoup
import re


class DotnetCrawlingManager(CrawlingManager):
    def __init__(self):
        super().__init__()
        

    def run(self):
        soup = self.soup
        cve_list = self._crawling_cve_data(soup)
        patch_data_list = self._crawling_patch_data(soup)

        # 각 기술문서 들어가서 제목 수집, 카탈로그 들어가서 패치파일 다운로드, 파일 이름 변경

    
    def _crawling_cve_data(self, soup: BeautifulSoup):
        return list(map(lambda x: re.match("CVE-\d+-\d+", x.text).group(), soup.find_all(id = re.compile("^cve"))))


    def _crawling_patch_data(self, soup: BeautifulSoup):
        table = soup.find("table")
        tbody = table.find("tbody")
        tds = tbody.find_all("td")

        tmp = dict()
        last_key = ""

        for td in tds:
            # 공백 td 제거
            if td.text.strip() == "":
                continue
            
            # Microsoft | Windows로 시작하면 Product Version
            if td.text.startswith("Microsoft") or td.text.startswith("Windows"):
                tmp[td.text] = list()   
                last_key = td.text

            # 숫자로 시작하면 qnumber
            if td.text.startswith("503"):
                if td.find("strong") != None:
                    print(f"부모 QNumber 제외합니다. {td.text}")
                
                # 이 시점에 Key가 무조건 존재함
                tmp[last_key].append({
                    "catalog_link": f"http://www.catalog.update.microsoft.com/Search.aspx?q={td.text}",
                    "bulletin_url_kr": f"http://support.microsoft.com/ko-kr/help/{td.text}",
                    "bulletin_url_jp": f"http://support.microsoft.com/ja-jp/help/{td.text}",
                    "bulletin_url_us": f"http://support.microsoft.com/en-us/help/{td.text}",
                    "bulletin_url_cn": f"http://support.microsoft.com/zh-cn/help/{td.text}",
                })
                

            # 카탈로그 링크
            # http://www.catalog.update.microsoft.com/Search.aspx?q={qnumber}
                
            # 기술문서 링크
            # http://support.microsoft.com/{nation-code}/help/{qnumber}
        
        return tmp
            

if __name__ == "__main__":
    dcm = DotnetCrawlingManager()
    dcm.run()