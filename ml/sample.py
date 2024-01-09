import numpy as np
import pandas as pd
import json
import os
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
            df = pd.read_csv("https://bit.ly/perch_csv_data")
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
            fish = pd.read_csv("https://bit.ly/fish_csv_data")
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


if __name__ == "__main__":
    sp = Sample()
    # print(sp.read_remote_perch_data())
    print(sp.read_remote_fish_data())