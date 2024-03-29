import numpy as np
import pandas as pd
import json
import os
import threading
from sklearn.model_selection import train_test_split


class Sample:
    _json_file_path = r"C:\Users\seungsu\Desktop\projects\unittest\ml\data.json"
    
    # json keys
    perch_length = "perch_length"
    perch_weight = "perch_weight"
    bream_length = "bream_length"
    bream_weight = "bream_weight"
    smelt_length = "smelt_length"
    smelt_weight = "smelt_weight"
    perch_full = "perch_full"
    fish_full = "fish_full"

    def __init__(self):
        if not os.path.exists(self._json_file_path):
            print(f"해당 파일을 찾을 수 없습니다. path: {self._json_file_path}")
            return
        
        with open(self._json_file_path, encoding="utf8") as f:
            self.json_obj = json.load(f)    

        print("샘플 데이터 로딩이 완료되었습니다....")


    def get_perch_data(self):
        return self.perch_length, self.perch_weight


    def get_sample_data(self):
        train_input, test_input, train_target, test_target = train_test_split(
            np.array(self.json_obj[self.perch_length]),
            np.array(self.json_obj[self.perch_weight]), 
            random_state = 42
        )
    
        # 훈련 세트는 2차원 배열이여야 하므로 shape 변경
        train_input = train_input.reshape(-1, 1)
        test_input = test_input.reshape(-1, 1)

        return train_input, test_input, train_target, test_target
    
    
    def get_bream_smelt_data(self):
        return (
            self.json_obj[self.bream_length], 
            self.json_obj[self.bream_weight], 
            self.json_obj[self.smelt_length], 
            self.json_obj[self.smelt_weight]
        )


    def get_fish_data(self):
        fish_length = np.append(self.json_obj[self.bream_length], self.json_obj[self.smelt_length])
        fish_weight = np.append(self.json_obj[self.bream_weight], self.json_obj[self.smelt_weight])

        return fish_length, fish_weight
    

    def read_remote_perch_data(self):
        if self.perch_full not in self.json_obj:
            df = self.call_network_thread("https://bit.ly/perch_csv_data")
            perch_full = df.to_numpy()

            length = list(perch_full[:, 0])
            height = list(perch_full[:, 1])
            width = list(perch_full[:, 2])

            self.json_obj[self.perch_full] = {
                "length": length,
                "height": height,
                "width": width
            }
            
            with open(self._json_file_path, "w", encoding="utf8") as fp:
                json.dump(self.json_obj, fp, sort_keys = True, indent = 4)

        perch_dict = self.json_obj[self.perch_full]
        perch_full_data = np.column_stack((perch_dict["length"], perch_dict["height"], perch_dict["width"]))
        perch_weight_data = np.array(self.json_obj[self.perch_weight])

        return perch_full_data, perch_weight_data


    def read_remote_fish_data(self):
        if self.fish_full not in self.json_obj:
            fish = self.call_network_thread("https://bit.ly/fish_csv_data")
            fish_dict = dict()

            for col in fish.columns:
                fish_dict[col] = list(fish[col].to_numpy())

            self.json_obj[self.fish_full] = fish_dict

            with open(self._json_file_path, "w", encoding="utf8") as fp:
               json.dump(self.json_obj, fp, sort_keys = True, indent = 4)

        fish_full = self.json_obj[self.fish_full]

        fish_input = np.column_stack((
            fish_full["Weight"],
            fish_full["Length"],
            fish_full["Diagonal"],
            fish_full["Height"],
            fish_full["Width"]
        ))

        fish_target = np.array(fish_full['Species'])

        return fish_input, fish_target
    

    def read_remote_wine_data(self):
        url = "https://raw.githubusercontent.com/rickiepark/hg-mldl/master/wine.csv"
        wine = self.call_network_thread(url)

        # 첫 5개 샘플을 확인하고, 데이터프레임의 각 열의 데이터 타입과 누락 데이터 확인
        # 만약 누락된 데이터가 있다면 훈련 세트의 평균값으로 채워 사용하는 방법이 있다.
        print(wine.head())  
        print(wine.info())  
        
        # 각 열에 대한 간략한 통계 출력 (최대, 최소, 평균, 표준편차, n분위수)
        print(wine.describe())

        # 데이터 프레임을 넘파이 배열로 바꾸어 리턴
        wine_data = wine[['alcohol', 'sugar', 'pH']].to_numpy()
        wine_target = wine['class'].to_numpy()

        return wine_data, wine_target
    

    def call_network_thread(self, url):
        thread = ThreadWithReturnValue(target = self._call_remote_data, args = [url])
        thread.start()
        print(f"Thread {thread.name} 실행")
        return thread.join()


    def _call_remote_data(self, url: str):
        return pd.read_csv(url)


# 네트워크 I/0를 위한 스레드 상속 클래스 
class ThreadWithReturnValue(threading.Thread):
    def __init__(self, group = None, target = None, name = None, args = (), kwargs = {}, verbose = None):
        threading.Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self, *args):
        threading.Thread.join(self, *args)
        return self._return
        


if __name__ == "__main__":
    sp = Sample()
    sp.read_remote_fish_data()
    sp.read_remote_perch_data()
    sp.read_remote_wine_data()