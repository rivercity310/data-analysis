from crawling_manager import CrawlingManager
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import re
import requests
import time
import os




class DotnetCrawlingManager(CrawlingManager):
    test_link = "https://devblogs.microsoft.com/dotnet/dotnet-framework-january-2024-security-and-quality-rollup/"

    result_dict = dict()

    _exclude_patch = {
        "Microsoft server operating system, version 23H2": "*",
        "Windows 10 1607 and Windows Server 2016": ".NET Framework 3.5, 4.6.2, 4.7, 4.7.1, 4.7.2",
        "Windows 10 1507": "*"
    }

    _patch_file_path = "D:\\patch\\patchfiles"

    def __init__(self):
        super().__init__()
        self.download_click_cnt = 0
        

    def run(self):
        try:
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
            print("***vendor url 역시 수동으로 수집해주세요***")
            print("추후 완전 자동화로 개선될 예정입니다.")
            print("\n\n")

            """
            while True:
                res = input("전체 패치 파일을 다운로드 받으셨나요? (y/n) ")
                
                if res != "y":
                    continue

                if os.path.exists(self._patch_file_path):
                    if self.download_click_cnt == len(os.listdir()):
                        print("전체 파일 다운로드가 확인되었습니다.")
                        break
            """

            # 패치 파일명 변경, 패치 파일 압축 해제, WSUSSCAN 파일명 변경 & 추출 작업
            for file_name in os.listdir(self._patch_file_path):
                if not file_name.startswith("windows"):
                    continue

                sp = file_name.split("_")
                new_file_name = "".join([sp[0], ".", sp[1].split(".")[1]]).replace("kb", "KB")
                print(f"[파일명 변경] {file_name} -> {new_file_name}")

                file_abs_path = f"{self._patch_file_path}\\{new_file_name}"
                os.rename(f"{self._patch_file_path}\\{file_name}", file_abs_path)

                # msu 파일 압축해제
                cmd = f"expand -f:* {file_abs_path} D:\\patch\\{new_file_name}"
                os.system(cmd)
                os.rename(f"D:\\patch\\{new_file_name}\\WSUSSCAN.cab", f"D:\\patch\\{new_file_name}\\{new_file_name.split('.msu')[0]}_WSUSSCAN.cab")
                
        
        except Exception as e:
            print("--------------- 처리되지 않은 예외 발생 --------------")
            print(e)
            print("--------------- 프로그램이 비정상적으로 종료되었습니다.")
            
            # 추후 패치파일 다운로드 폴더 삭제 및 데이터 해제 작업 진행
            # self.rollback()

        finally:
            self.browser.close()
            # self.write_result()

    
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
                        print(f"****{product_version} 전체 제외합니다.")
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
                    print(f"****부모 QNumber 제외합니다. {qnumber}")
                    continue

                if qnumber in qnumbers:
                    print(f"****이미 처리된 QNumber 제외합니다. {qnumber}")
                    continue

                # 카탈로그 링크: http://www.catalog.update.microsoft.com/Search.aspx?q={qnumber}
                # 기술문서 링크: http://support.microsoft.com/{nation-code}/help/{qnumber}
                print(f"[타겟 QNumber를 발견했습니다]: {qnumber}")

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
            print("--------------------------- 예외 발생 -------------------------")
            print(e)
            return "Can't find Title", "Can't find Summary"
        
        return title, summary


    def _download_patch_file(self, link):
        try:
            browser = self.browser
            browser.get(link)
            table = self.browser.find_element(by = By.CLASS_NAME, value = "resultsBorder")
            trs = table.find_elements(by = By.TAG_NAME, value = "tr")[1:]

            for tr in trs:
                tds = tr.find_elements(by = By.TAG_NAME, value = "td")[1:]
                download_link = tds[-1]
                download_link.click()
                self.download_click_cnt += 1
                # browser.implicitly_wait(2)
                time.sleep(2)
        
        except Exception as e:
            print(f"에러가 발생했습니다. {link}")
            print(e)
            return
            

if __name__ == "__main__":
    dcm = DotnetCrawlingManager()
    # dcm.run()
    print(dcm._crawling_patch_title_and_summary("https://support.microsoft.com/ko-kr/help/5018210"))

    # 패치 파일명 변경, 패치 파일 압축 해제, WSUSSCAN 파일명 변경 & 추출 작업
    '''
    path = "D:\\patch\\patchfiles"

    for file_name in os.listdir(path):
        if not file_name.startswith("windows"):
            continue

        sp = file_name.split("_")
        new_file_name = "".join([sp[0], ".", sp[1].split(".")[1]]).replace("kb", "KB")

        os.rename(path + "\\" + file_name, path + "\\" + new_file_name)
        
        file_abs_path = path + "\\" + new_file_name
        file_unzip_path = file_abs_path + "\\" + new_file_name

        os.mkdir(f"D:\\patch\\{new_file_name}")

        cmd = "expand -f:* " + file_abs_path + " " + f"D:\\patch\\{new_file_name}"
        print(f"명령어 실행: {cmd}")
        os.system(cmd)

        os.rename(f"D:\\patch\\{new_file_name}\\WSUSSCAN.cab", f"D:\\patch\\{new_file_name}\\{new_file_name.split('.msu')[0]}_WSUSSCAN.cab")
    '''
    
    
                