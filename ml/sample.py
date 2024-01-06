import numpy as np
import json
import os
from sklearn.model_selection import train_test_split


class Sample:
    def __init__(self):
        json_file_path = r"C:\Users\seungsu\Desktop\projects\unittest\ml\data.json"

        if not os.path.exists(json_file_path):
            print(f"해당 파일을 찾을 수 없습니다. path: {json_file_path}")
            return
        
        with open(json_file_path, encoding="utf8") as f:
            json_obj = json.load(f)    
            self.perch_length = np.array(json_obj["perch_length"])
            self.perch_weight = np.array(json_obj["perch_weight"])
            self.bream_length = np.array(json_obj["bream_length"])
            self.bream_weight = np.array(json_obj["bream_weight"])
            self.smelt_length = np.array(json_obj["smelt_length"])
            self.smelt_weight = np.array(json_obj["smelt_weight"])
            print("샘플 데이터 로딩이 안료되었습니다....")


    def get_perch_data(self):
        return self.perch_length, self.perch_weight


    def get_sample_data(self):
        train_input, test_input, train_target, test_target = train_test_split(
            self.perch_length, self.perch_weight, random_state=42
        )
    
        # 훈련 세트는 2차원 배열이여야 하므로 shape 변경
        train_input = train_input.reshape(-1, 1)
        test_input = test_input.reshape(-1, 1)

        return train_input, test_input, train_target, test_target
    
    
    def get_bream_smelt_data(self):
        return self.bream_length, self.bream_weight, self.smelt_length, self.smelt_weight


if __name__ == "__main__":
    sp = Sample()