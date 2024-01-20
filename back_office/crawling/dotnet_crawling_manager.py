from crawling_manager import CrawlingManager
from bs4 import BeautifulSoup
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from typing import List, Set, Dict, Tuple
from pathlib import Path
import re
import time
import os
import hashlib
import json
import math


# TODO
# 1. _patch_files_path 폴더 비우기 작업 -> 완료
# 2. 추출된 Title, Summary에서 특정 유니코드 제거 작업 (문자열화) ex. - : \u2013
# 3. 중요도 수집
# 4. 코드 모듈화
# 5. CVE번호 MSRC에 검색해서 검증하기
# 6. 제품명에 따른 다운로드 예외 처리 (https://www.catalog.update.microsoft.com/Search.aspx?q=5034119) 링크에서 Windows Server 2016 -> 완료
# 7. 예외 발생시 수집 Title, Summary


class DotnetCrawlingManager(CrawlingManager):
    def __init__(self):
        super().__init__()
        
        self._cab_file_path = self._patch_file_path / "cabs"
        self.qnumbers: Dict[str, Tuple[str, str, BeautifulSoup]] = dict()
        self.patch_info_dict: Dict[str, Dict[str, str]] = dict()
        self.error_patch_dict = dict()


    def _extract_file_info(self, file_name, vendor_url):
        time.sleep(3)

        file_abs_path = self._patch_file_path / file_name

        if not os.path.exists(self._cab_file_path):
            os.mkdir(self._cab_file_path)

        # 파일 크기
        size_tmp = float(f"{os.path.getsize(file_abs_path) / (2 ** 20):.2f}")
        file_size = math.floor(size_tmp + 0.5)

        with open(file_abs_path, "rb") as fp:
            binary = fp.read()
            md5 = hashlib.md5(binary).hexdigest()
            sha256 = hashlib.sha256(binary).hexdigest()

        # msu 파일 압축해제 (WSUSSCAN 파일만)
        cmd = f"expand -f:* {file_abs_path} {self._cab_file_path}"
        cab_file_name = file_name.split(".msu")[0] + "_WSUSSCAN.cab"
        os.system(cmd)
        time.sleep(3)

        os.rename(self._cab_file_path / "WSUSSCAN.cab", self._cab_file_path / cab_file_name)

        return {
            "file_size": file_size,
            "vendor_url": vendor_url,
            "WSUS 파일": cab_file_name,
            "MD5": md5,
            "SHA256": sha256
        }


    def _get_cve_string(self):
        div = self.soup.find("div", "entry-content")
        cve_list = list(map(lambda x: re.match("CVE-\d+-\d+", x.text).group(), div.find_all(id = re.compile("^cve"))))
        return ",".join(cve_list)

        
    def _crawling_patch_title_and_summary(self, url):
        try:
            self.driver.get(url)
            self.driver.implicitly_wait(5)
            soup = BeautifulSoup(self.driver.page_source, "html.parser")

            title = soup.find(name = "h1", attrs = {"id": "page-header"}).text.strip()
            section = soup.find(name = "section", attrs = {"id": "bkmk_summary"})
            ps = section.find_all(name = "p")
            
            summary = ""
            for p in ps:
                if p.text.strip().startswith("CVE"):
                    summary += p.text.strip() + "\n"
        
        except Exception as e:
            print("--------------------------- 예외 발생 -------------------------")
            print(e)
            return "Can't find Title", "Can't find Summary"
        
        return title, summary


    def _download_patch_file(self) -> Dict[str, str]:
        driver = self.driver
        file_dict = dict()
        
        for qnumber, value in self.qnumbers.items():
            product_version = value[0]
            dotnet_version = value[1]
            catalog_elem = value[2]

            file_dict[qnumber] = list()
            self.error_patch_dict[qnumber] = list()            

            try:
                link = str(catalog_elem['href'])
                driver.get(link)
                self._driver_wait(By.CLASS_NAME, "resultsBorder")
                main_window = driver.current_window_handle

                table: WebElement = driver.find_element(by = By.CLASS_NAME, value = "resultsBorder")
                trs: List[WebElement] = table.find_elements(by = By.TAG_NAME, value = "tr")[1:]

                os.system("cls")

                print(f"[{product_version} {dotnet_version}] 다운로드 작업 시작")
                print("link: ", link)

                for tr in trs:
                    self._driver_wait(By.TAG_NAME, "td")
                    tds: List[WebElement] = tr.find_elements(by = By.TAG_NAME, value = "td")[1:]
                    tds[-1].click()
                    time.sleep(2)

                while len(driver.window_handles) != 1:
                    driver.switch_to.window(driver.window_handles[-1])

                    # 열린 다운로드 창에서 파일 다운로드 받기
                    xpath = "//*[@id=\"downloadFiles\"]/div[2]/a"
                    self._driver_wait(By.XPATH, xpath)
                    
                    atag: WebElement = driver.find_element(by = By.XPATH, value = xpath)
                    vendor_url = atag.get_attribute('href')
                    file_name = self._msu_file_name_change(atag.text)

                    if self._is_already_exists(atag.text):
                        print("\n\t[INFO] 중복된 파일 제외")
                        print(f"\t{file_name}")
                        driver.close()
                        continue
                    
                    atag.click()

                    print("\n\t------------ [Downloading] ---------------")
                    print(f"\t[파일명] {file_name}")
                    print(f"\t[Vendor URL] {vendor_url}")
                    print("\t--------------------------------------------\n")
                    
                    file_dict[qnumber].append({
                        "file_name": file_name,
                        "vendor_url": vendor_url,
                        "catalog": link,
                        "product": product_version,
                        "version": dotnet_version,
                    })

                    time.sleep(4)
                    driver.close()
                
                # 다시 main window로 전환 (카탈로그 창)
                driver.switch_to.window(main_window)
                
                # 다운로드 완료 대기 
                self._wait_til_download_ended()

            except Exception as e:
                print(f"\"{link}\"를 처리하던 중 에러가 발생했습니다.")
                print(e)

                self.error_patch_dict[qnumber].append({
                    "product": product_version,
                    "version": dotnet_version,
                    "catalog": link,
                    "message": e
                })

                continue
        
            finally:
                # msu 파일명 전부 변경
                print("\n[INFO] .msu 파일명에서 해시값 제거")

                for file in os.listdir(self._patch_file_path):
                    renamed = self._msu_file_name_change(file)
                    os.rename(self._patch_file_path / file, self._patch_file_path / renamed)
                    print(f"\t{file} -> {renamed}")

        return file_dict
    

    # 수집할 OS 대상, QNUMBER, CATALOG URL을 미리 수집해두고 시작
    def _init_patch_data(self) -> None:
        # patch_info_dict 구조
        """
        {
            "Microsoft server operation system, version 22H2": [
                (".NET Framework 3.5, 4.8", "5033912"),
                (".NET Framework 3.5, 4.8.1", "5033914")
                ...
            ],
            
            ...
        }
        """
        
        patch_info_dict = self.patch_info_dict
        soup = self.soup
        qnumbers = self.qnumbers

        tbody: BeautifulSoup = soup.find("table").find("tbody")
        tds: List[BeautifulSoup] = tbody.find_all("td") 
        
        last_product_key = ""
        last_dotnet_key = ""
        last_catalog_link = ""
        
        for td in tds:
            tstrip = td.text.strip()
            is_parent_kb = td.find("strong") != None and tstrip.startswith("50")
            
            # 공란 무시
            if tstrip == "":
                continue
            
            # KBNumber 중 Bold 처리된 것은 부모 KBNumber이므로 무시
            if is_parent_kb:
                continue
            
            # Microsoft 혹은 Windows로 시작하면 Product Version을 나타냄
            if tstrip.startswith("Microsoft") or tstrip.startswith("Windows"):
                patch_info_dict[tstrip] = list()
                last_product_key = tstrip 
            
            # .NET으로 시작하면 .NET 버전을 나타냄
            elif tstrip.startswith(".NET"):
                if last_product_key == "":
                    raise Exception("[ERR] 마지막으로 검색된 Product Version이 존재하지 않습니다.")
                
                last_dotnet_key = tstrip

            # Catalog 링크 수집
            elif tstrip.startswith("Catalog"):
                href = td.findChild("a")
                last_catalog_link = href
            
            # 자식 KBNumber인 경우
            elif re.match("^50\d{5}", tstrip):
                if last_product_key == "" or last_dotnet_key == "":
                    raise Exception("[ERR] 마지막으로 검색된 Product Version 혹은 .NET Version이 존재하지 않습니다.")
                
                if tstrip not in qnumbers:
                    qnumbers[tstrip] = (last_product_key, last_dotnet_key, last_catalog_link)
                    patch_info_dict[last_product_key].append((last_dotnet_key, tstrip))

        # 빈 Product Version 삭제
        tmp = list()
        for product in patch_info_dict:
            if len(patch_info_dict[product]) == 0:
                tmp.append(product)
        
        for product in tmp:
            del patch_info_dict[product]
        

    def _show_prompt(self) -> None:
        def _remove_patch(removed: str):
            if removed not in self.qnumbers:
                print(f"[{removed}] 목록에 없는 QNumber 입니다.")
                return

            info = self.qnumbers[removed]
            product_version = info[0]
            dotnet_version = info[1]
            tmp = list()

            for tup in self.patch_info_dict[product_version]:
                if tup[1] == removed:
                    self.patch_info_dict[product_version].remove((dotnet_version, removed))

                    if len(self.patch_info_dict[product_version]) == 0:
                        tmp.append(product_version)

            for t in tmp:
                del self.patch_info_dict[t]

            del self.qnumbers[removed]

        patch_info_dict = self.patch_info_dict

        while True:
            print("\n\n-------------------- 패치 대상 정보가 수집되었습니다 ----------------------")
            for product in patch_info_dict:
                print(product)
                for data in patch_info_dict[product]:
                    version = data[0]
                    qnumber = data[1]
                    print(f"\t[{qnumber}] {version}")
                print()
            print("------------------------------------------------------------------------\n\n")

            res = input("제외할 패치의 QNumber를 입력해주세요. (여러개인 경우 ','로 구분하여 입력하고 없으면 'n' 입력) : ")

            if res == 'n':
                break

            for removed in res.split(","):
                print(f"[removed] {removed.strip()} 삭제")
                _remove_patch(removed.strip())


    def _get_patch_date(self) -> str:
        date_elem = self.soup.find("em").find("strong")
        
        if date_elem == None:
            raise Exception("패치 날짜 정보를 가져올 수 없습니다.")
        
        date = date_elem.text[1:-1].strip().split("/")
        return f"{date[-1]}/{date[0]}/{int(date[1]) + 1}"


    def test(self) -> None:
        # 패치 대상 데이터 초기화
        self._init_patch_data()
        
        # 프롬프트 출력, 패치 대상 데이터 최종 결정(제거)
        self._show_prompt()
        os.system("pause")
        
        # 프롬프트 창 clear
        os.system("cls")

        # 패치 날짜 정보 가져오기 (TODO 문서마다 다름)
        print("------------------------------------------")
        # patch_date = self._get_patch_date()
        # print("[Patch Date]", patch_date)

        # 패치 CVE 문자열 가져오기
        # 이 이후로 soup 객체를 사용하지 않으므로 메모리 해제
        cve_string = self._get_cve_string()
        print("[CVE List]", cve_string)
        del self.soup
        print("------------------------------------------\n\n")

        # 패치 대상의 각 카탈로그 링크에서 패치 파일 다운로드
        # 각 패치 파일 이름과 vendor URL에 대한 Dict 반환
        file_dict = self._download_patch_file()

        print("\n[INFO] 패치 파일 다운로드 작업 완료")
        self._save_result(self._crawling_dir_path / "file_dict.json", file_dict)

        print(self.error_patch_dict)
        for key in self.error_patch_dict:
            print("--------------------------------------")
            print(key, ": ")

            for params in self.error_patch_dict[key]:
                for param in params:
                    print(f"\t{param}: {params[param]}")

            print("--------------------------------------")

        # 메모리 해제
        self._del_driver()

    
    def _msu_file_name_change(self, name: str) -> str:
        return name.split("_")[0].replace("kb", "KB") + ".msu" 
        

if __name__ == "__main__":
    dcm = DotnetCrawlingManager()
    dcm.test()
