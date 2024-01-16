from crawling_manager import CrawlingManager
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from collections import deque
from datetime import datetime
import re
import requests
import time
import os
import hashlib
import json


class DotnetCrawlingManager(CrawlingManager):
    test_link = "https://devblogs.microsoft.com/dotnet/dotnet-framework-january-2024-security-and-quality-rollup/"


    _exclude_patch = {
        "Microsoft server operating system, version 23H2": "*",
        "Windows 10 1607 and Windows Server 2016": ".NET Framework 3.5, 4.6.2, 4.7, 4.7.1, 4.7.2",
        "Windows 10 1507": "*"
    }

    _patch_file_path = "D:\\patch\\patchfiles"


    def __init__(self):
        super().__init__()
        self.download_click_cnt = 0
        self.qnumbers = deque()
        self.result_dict = dict()
        self.main_window = self.browser.window_handles[0]

        # TODO
        # 1. _patch_files_path 폴더 비우기 작업
        # 2. 추출된 Title, Summary에서 유니코드 제거 작업 (문자열화)
        # 3. 중요도 수집
        # 4. 코드 모듈화
        # 5. CVE번호 MSRC에 검색해서 검증하기

    def run(self):
        try:
            time.sleep(5)
            print("-------------------- 닷넷 크롤러를 작동합니다 ---------------------------------")
            soup = self.soup

            # 전체 공통 속성 
            # PatchDate, CVE
            global_commons = dict()
    
            print("-----------[패치 노트 CVE 목록 수집중...]--------------")
            cve_list = self._crawling_cve_data(soup)
            print(",".join(cve_list))
            print("-----------[CVE 목록 수집 완료]-----------------------")
            print("\n\n")

            print("------[catalog url, qnumber, bulletin url 수집중...]-----")
            patch_data_dict = self._crawling_patch_data(soup)
            print("-----------------------[수집 완료]-----------------------")
            print("\n\n")

            global_commons["commons"] = dict()
            global_commons["commons"]["PatchDate"] = datetime.today().strftime("%Y/%m/%d")
            global_commons["commons"]["cve"] = ",".join(cve_list)

            # 빈 리스트 키 삭제 & 딥카피
            data_dict = dict(filter(lambda val: len(val[1]) != 0, patch_data_dict.items()))
            del patch_data_dict

            # 각 기술문서 들어가서 제목 수집, 카탈로그 들어가서 패치파일 다운로드, 파일 이름 변경
            print("-----[각 기술문서에서 Title, Summary 수집, 카탈로그 다운로드 창 오픈중...]--------")

            for patch_key, patch_data in data_dict.items():
                print(f"[{patch_key} 작업을 시작합니다..]")
                global_commons[patch_key] = dict()

                # 각 라인별 공통 속성
                # BulletinID, KBNumber, 중요도
                local_commons = dict()
                last_qnum = ""

                # 각 라인 내에서 국가별로 다른 속성
                # title, summary, bulletinUrl
                diff = dict()

                for patch in patch_data:
                    for data_key, data_value in patch.items():  
                        print(f"{data_key} : {data_value}")

                        if data_key.startswith("catalog"):
                            print(f"Catalog Open: {data_value}")
                            
                            vendor_dict = self._download_patch_file(data_value)

                            while True: 
                                dl = False
                                for file in os.listdir(self._patch_file_path):
                                    if file.endswith("crdownload"):
                                        dl = True

                                print("아직 파일을 다운로드 하고있어요...............")
                                time.sleep(2)

                                if not dl:
                                    break

                            for file_name, vendor_url in vendor_dict.items():
                                print(f"{file_name} : {vendor_url}")

                                # 여기서 가공해야 함 key = file_name, value = SHA256, MD5, vendor_url, file_size, wsusscan
                                sp = file_name.split("_")
                                new_file_name = "".join([sp[0], ".", sp[1].split(".")[1]]).replace("kb", "KB")

                                print(f"[파일명 변경] {file_name} -> {new_file_name}")
                                file_abs_path = f"{self._patch_file_path}\\{new_file_name}"

                                try:
                                    os.rename(f"{self._patch_file_path}\\{file_name}", file_abs_path)
                                
                                except Exception as e:
                                    print("--------파일명 변경 중 에러 발생!! (중복된 파일)------------")
                                    print(f"\"{file_name}\": 건너뜁니다")
                                    continue

                                global_commons[patch_key][new_file_name] = self.extract_file_info(new_file_name, vendor_url) 

                            qnum = data_value[-7:]
                            local_commons[qnum] = dict()
                            local_commons[qnum]["Bulletine ID"] = f"MS-KB{qnum}"
                            local_commons[qnum]["KBNumber"] = f"KB{qnum}"
                            local_commons[qnum]["중요도"] = "???"       
                            last_qnum = qnum
                
                        elif data_key.startswith("bulletin"):
                            print(f"기술문서 Open: {data_value}")
                            title, summary = self._crawling_patch_title_and_summary(data_value)
                            print(f"title: {title}")
                            print(f"summary: {summary}")
                            
                            diff[last_qnum] = dict()
                            postfix = data_key[-3:] # _kr, _en ..
                            
                            bulletin_key = "BulletinUrl" + postfix
                            title_key = "Title" + postfix
                            summary_key = "Summary" + postfix
                            
                            diff[last_qnum][bulletin_key] = data_value
                            diff[last_qnum][title_key] = title
                            diff[last_qnum][summary_key] = summary

                global_commons[patch_key]["local_commons"] = local_commons
                global_commons[patch_key]["diff"] = diff

                print(global_commons)


            # CAB 파일 정리
            cab_file_path = self._patch_file_path + "\\" + "cabs"
            for file in os.listdir(cab_file_path):
                # KB 단위
                file_size = os.path.getsize(cab_file_path + "\\" + file) / (10 ** 4)

                if file_size <= 10 or file_size >= 1000:
                    print(f"{file} -> 불필요한 삭제!")
                    os.remove(cab_file_path + "\\" + file)


            print("-----------------------[수집 완료]-----------------------")
            print("\n\n")

            with open("D:\\patch\\result.json", "w", encoding = "utf8") as fp:
                json.dump(global_commons, fp, indent = 4, sort_keys = True)

            while True:
                res = input("전체 패치 파일을 다운로드 받으셨나요? (y/n) ")
                
                if res != "y":
                    continue

                if os.path.exists(self._patch_file_path):
                    if self.download_click_cnt == len(os.listdir()):
                        print("전체 파일 다운로드가 확인되었습니다.")
                        break

        except Exception as e:
            print("--------------- 처리되지 않은 예외 발생 --------------")
            print(e)
            print("--------------- 프로그램이 비정상적으로 종료되었습니다.")
            
            # 추후 패치파일 다운로드 폴더 삭제 및 데이터 해제 작업 진행
            # self.rollback()

        finally:
            del self
            # self.write_result()


    def extract_file_info(self, file_name, vendor_url):
        time.sleep(3)

        file_abs_path = self._patch_file_path + "\\" + file_name
        cabs_file_path = self._patch_file_path + "\\" + "cabs"

        if not os.path.exists(cabs_file_path):
            os.mkdir(cabs_file_path)

        # 파일 크기
        file_size = f"{os.path.getsize(file_abs_path) / (10 ** 6):.2f}"

        with open(file_abs_path, "rb") as fp:
            binary = fp.read()
            md5 = hashlib.md5(binary).hexdigest()
            sha256 = hashlib.sha256(binary).hexdigest()

        # msu 파일 압축해제 (WSUSSCAN 파일만 )
        cmd = f"expand -f:* {file_abs_path} {cabs_file_path}"
        cab_file_name = file_name.split(".msu")[0] + "_WSUSSCAN.cab"
        os.system(cmd)
        time.sleep(3)

        os.rename(f"{cabs_file_path}\\WSUSSCAN.cab", f"{cabs_file_path}\\{cab_file_name}")

        return {
            "file_size": file_size,
            "vendor_url": vendor_url,
            "WSUS 파일": cab_file_name,
            "MD5": md5,
            "SHA256": sha256
        }


    def _crawling_cve_data(self, soup: BeautifulSoup):
        div = soup.find("div", "entry-content")
        return list(map(lambda x: re.match("CVE-\d+-\d+", x.text).group(), div.find_all(id = re.compile("^cve"))))


    def _crawling_patch_data(self, soup: BeautifulSoup):
        table = soup.find("table")
        tbody = table.find("tbody")
        tds = tbody.find_all("td")

        tmp = dict()
        last_keys = set()
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

            last_keys.add(last_key)

            # 숫자로 시작하면 qnumber
            if re.match("^\d{7}", td.text):
                qnumber = td.text

                if td.find("strong") != None:
                    print(f"****부모 QNumber 제외합니다. {qnumber}")
                    continue

                if qnumber in self.qnumbers:
                    print(f"****이미 처리된 QNumber 제외합니다. {qnumber}")
                    continue

                # 카탈로그 링크: http://www.catalog.update.microsoft.com/Search.aspx?q={qnumber}
                # 기술문서 링크: http://support.microsoft.com/{nation-code}/help/{qnumber}
                print(f"[타겟 QNumber를 발견했습니다]: {qnumber}")

                tmp[last_key].append({
                    "catalog_link": f"https://www.catalog.update.microsoft.com/Search.aspx?q={qnumber}",
                    "bulletin_url_kr": f"https://support.microsoft.com/ko-kr/help/{td.text}",
                    "bulletin_url_jp": f"https://support.microsoft.com/ja-jp/help/{td.text}",
                    "bulletin_url_us": f"https://support.microsoft.com/en-us/help/{td.text}",
                    "bulletin_url_cn": f"https://support.microsoft.com/zh-cn/help/{td.text}",
                })

                self.qnumbers.append(qnumber)

        print("------------------- 수집 대상 OS ----------------------------")
        for idx, key in enumerate(last_keys):
            print(f"{idx + 1}. {key}")
        print("-----------------------------------------------------------------")
        print("\n\n")
        
        return tmp
    

    def _crawling_patch_title_and_summary(self, url):
        try:
            self.browser.get(url)
            self.browser.implicitly_wait(5)
            soup = BeautifulSoup(self.browser.page_source, "html.parser")

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


    def _download_patch_file(self, link: str):
        browser = self.browser
        vendor_dict = dict()
        
        try:
            browser.get(link)
            table = browser.find_element(by = By.CLASS_NAME, value = "resultsBorder")
            trs = table.find_elements(by = By.TAG_NAME, value = "tr")[1:]
            download_path = self._patch_file_path
            main_window = browser.current_window_handle

            for tr in trs:
                tds = tr.find_elements(by = By.TAG_NAME, value = "td")[1:]
                title = tds[0].text
                print(f"{title} 클릭")
                download_link = tds[-1]
                download_link.click()

                time.sleep(3)

                browser.switch_to.window(browser.window_handles[-1]) 

                time.sleep(5)

                # 열린 다운로드 창에서 파일 다운로드 받기
                atag = browser.find_element(by = By.XPATH, value = "//*[@id=\"downloadFiles\"]/div[2]/a")
                vendor_url = atag.get_attribute('href')
                file_name = atag.text
                print(f"{file_name} : {vendor_url} 다운로드를 시도합니다.")

                if file_name in os.listdir(download_path):
                    print(f"[{file_name}] 이미 존재하는 파일은 건너뜁니다.")
                    browser.close()
                    browser.switch_to.window(main_window)
                    continue

                atag.click()
                self.download_click_cnt += 1
                vendor_dict[file_name] = vendor_url

                # 파일이 모두 다운로드 될 때까지 블로킹
                while True:
                    lst = os.listdir(self._patch_file_path)
                    dl = False

                    print("파일을 다운로드 중입니다..........")
                    for file in lst:
                        if file.endswith("crdownload"):
                            dl = True
                        else:
                            if file != "cabs" and file[-5] == ')':
                                os.remove(f"D:\\patch\\patchfiles\\{file}")
                        time.sleep(1)

                    if not dl:
                        break
                
                browser.close()
                browser.switch_to.window(main_window)

        except Exception as e:
            print(f"\"{link}\"를 처리하던 중 에러가 발생했습니다.")
            print(e)
        
        finally:
            for handle in browser.window_handles[1:]:
                browser.switch_to.window(handle)
                browser.close()
                del handle

            browser.switch_to.window(browser.window_handles[0])

        return vendor_dict
            

if __name__ == "__main__":
    dcm = DotnetCrawlingManager()
    dcm.run()
    # print(dcm._crawling_patch_title_and_summary("https://support.microsoft.com/ko-kr/help/5018210"))

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
    
    
                