from crawling_manager import CrawlingManager
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import re
import requests
import time


test_link = "https://devblogs.microsoft.com/dotnet/dotnet-framework-january-2024-security-and-quality-rollup/"


class DotnetCrawlingManager(CrawlingManager):
    result_dict = dict()

    _exclude_patch = {
        "Microsoft server operating system, version 23H2": "*",
        "Windows 10 1607 and Windows Server 2016": ".NET Framework 3.5, 4.6.2, 4.7, 4.7.1, 4.7.2",
        "Windows 10 1507": "*"
    }

    def __init__(self):
        super().__init__(test_link)
        

    def run(self):
        soup = self.soup
 
        print("-----------[패치 노트 CVE 목록 수집중...]--------------")
        cve_list = self._crawling_cve_data(soup)
        print(cve_list)
        print("-----------[CVE 목록 수집 완료]-----------------------")
        print("\n\n")

        print("------[catalog url, qnumber, bulletin url 수집중...]-----")
        patch_data_dict = self._crawling_patch_data(soup)
        print("-----------------------[수집 완료]-----------------------")
        print("\n\n")

        # 각 기술문서 들어가서 제목 수집, 카탈로그 들어가서 패치파일 다운로드, 파일 이름 변경
        print("-----[각 기술문서에서 Title, Summary 수집, 카탈로그 다운로드 창 오픈중...]--------")

        for patch_key, patch_data in patch_data_dict.items():
            print(f"[{patch_key} 작업을 시작합니다..]")

            for patch in patch_data:
                for data_key, data_value in patch.items():                
                    if data_key.startswith("catalog"):
                        print(f"Catalog Open: {data_value}")
                        self._download_patch_file(data_value)
            
                    elif data_key.startswith("bulletin"):
                        print(f"기술문서 Open: {data_value}")
                        title, summary = self._crawling_patch_title_and_summary(data_value)
                        print(f"title: {title}")
                        print(f"summary: {summary}")

        print("-----------------------[수집 완료]-----------------------")
        print("***패치 파일은 수동으로 다운로드 받아야 합니다***")
        print("\n\n")

    
    def _crawling_cve_data(self, soup: BeautifulSoup):
        return list(map(lambda x: re.match("CVE-\d+-\d+", x.text).group(), soup.find_all(id = re.compile("^cve"))))


    def _crawling_patch_data(self, soup: BeautifulSoup):
        table = soup.find("table")
        tbody = table.find("tbody")
        tds = tbody.find_all("td")

        tmp = dict()
        qnumbers = set()
        last_key = ""
        last_exclude_key = ""

        for td in tds:
            # 공백 td 제거
            if td.text.strip() == "":
                continue

            # Microsoft | Windows로 시작하면 Product Version
            if td.text.startswith("Microsoft") or td.text.startswith("Windows"):
                product_version = td.text.strip()

                if product_version in self._exclude_patch:
                    if self._exclude_patch[product_version] == "*":
                        print(f"{product_version} 전체 제외합니다.")
                        last_exclude_key = product_version
                        continue

                    last_exclude_key = product_version
                
                last_key = product_version
                tmp[last_key] = list()
                
            # product version의 특정 닷넷 패치를 제외
            if td.text.strip().startswith(".NET"):
                dotnet_version = td.text.strip()
                
                if last_exclude_key in self._exclude_patch:
                    if dotnet_version == self._exclude_patch[last_exclude_key]:
                        print(f"****[{last_exclude_key} : {dotnet_version}] 제외합니다.")
                        last_exclude_key = ""
                        continue
            
            if last_key == "":
                continue

            # 숫자로 시작하면 qnumber
            if re.match("^\d{7}", td.text):
                qnumber = td.text

                if td.find("strong") != None:
                    print(f"부모 QNumber 제외합니다. {qnumber}")
                    continue

                if qnumber in qnumbers:
                    print(f"이미 처리된 QNumber 제외합니다. {qnumber}")
                    continue

                # 카탈로그 링크: http://www.catalog.update.microsoft.com/Search.aspx?q={qnumber}
                # 기술문서 링크: http://support.microsoft.com/{nation-code}/help/{qnumber}
                print(f"타겟 QNumber를 발견했습니다. QNumber = {qnumber}")

                tmp[last_key].append({
                    "catalog_link": f"http://www.catalog.update.microsoft.com/Search.aspx?q={qnumber}",
                    "bulletin_url_kr": f"http://support.microsoft.com/ko-kr/help/{td.text}",
                    "bulletin_url_jp": f"http://support.microsoft.com/ja-jp/help/{td.text}",
                    "bulletin_url_us": f"http://support.microsoft.com/en-us/help/{td.text}",
                    "bulletin_url_cn": f"http://support.microsoft.com/zh-cn/help/{td.text}",
                })

                qnumbers.add(qnumber)
        
        return tmp
    

    def _crawling_patch_title_and_summary(self, url):
        try:
            req = requests.get(url)
            req.raise_for_status()
            soup = BeautifulSoup(req.content, "html.parser")

            title = soup.find(name = "h1", attrs = {"id": "page-header"}).text.strip()
            section = soup.find(name = "section", attrs = {"id": "bkmk_summary"})
            ps = section.find_all(name = "p")

            print("--------------------------------")
            print(f"url: {url}")
            print(f"title: {title}")
            
            summary = ""
            for p in ps:
                if p.text.strip().startswith("CVE"):
                    summary += p.text.strip() + "\n"
            print(summary.rstrip())
            print("--------------------------------")
        
        except Exception as e:
            print("----------- 예외 발생 ----------")
            print(e)
            return title, "Can't find summary"
        
        return title, summary


    def _download_patch_file(self, link):
        browser = self.browser
       
        browser.get(link)
        table = self.browser.find_element(by = By.CLASS_NAME, value = "resultsBorder")
        trs = table.find_elements(by = By.TAG_NAME, value = "tr")[1:]

        for tr in trs:
            tds = tr.find_elements(by = By.TAG_NAME, value = "td")[1:]
            download_link = tds[-1]
            download_link.click()
            # browser.implicitly_wait(2)
            time.sleep(2)
            

if __name__ == "__main__":
    dcm = DotnetCrawlingManager()
    dcm.run()