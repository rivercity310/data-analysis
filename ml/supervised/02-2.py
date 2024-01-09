# [ 데이터 전처리 ]
# - 두 특성(길이와 무게)의 값이 놓인 범위가 다를 때 발생 (= 두 특성의 스케일이 다르다)
# - 가로축과 세로축의 스케일을 맞추어야 함 (특히 알고리즘이 거리 기반인 경우)

# [ 전처리 방법 ]
# 표준점수(Z 점수)
#   - 각 특성값이 평균으로부터 표준편차의 몇 배만큼 떨어져 있는지 나타냄
#   - 이를 통해 실제 특성값의 크기와 상관없이 동일한 조건으로 비교 가능


import numpy as np
import matplotlib.pyplot as plt
from sample import Sample
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier


class KNeighbors_02_2_Ex:
    def __init__(self):
        sample = Sample()
        fish_length, fish_weight = sample.get_fish_data()
        fish_data = np.column_stack((fish_length, fish_weight))
        fish_target = np.concatenate((np.ones(35), np.zeros(14)))

        # 기본적으로 25%를 테스트 세트로 떼어냄
        # 일부 클래스의 개수가 적은 경우 샘플링 편향이 나타날 수 있음
        #   - stratify: 타깃 데이터를 전달하면 클래스 비율에 맞게 데이터를 나눔
        # random_state: 랜덤 시드 지정
        tmp = train_test_split(fish_data, fish_target, stratify=fish_target, random_state=42)

        self.train_input = tmp[0]
        self.test_input = tmp[1]
        self.train_target = tmp[2]
        self.test_target = tmp[3]


    def ex1(self):
        sp = [[25, 150]]

        kn = KNeighborsClassifier()
        kn.fit(self.train_input, self.train_target)
        print(kn.score(self.test_input, self.test_target))
        print(kn.predict(sp))  # 예측 이상

        # 이상치 데이터에 대해 산점도 그려보기
        plt.scatter(self.train_input[:, 0], self.train_input[:, 1])
        plt.scatter(sp[0][0], sp[0][1], marker="^")     # marker: 모양 지정
        plt.xlabel("length")
        plt.ylabel("weight")

        # 이상치 샘플의 주변 샘플 찾아보기
        # kneighbors(): n_neighbors 수 만큼 이웃까지의 거리와 이웃 샘플의 인덱스 반환 
        distances, indexes = kn.kneighbors(sp) 
        print(distances, indexes)
        plt.scatter(self.train_input[indexes, 0], self.train_input[indexes, 1], marker="D")
        plt.show()


    def ex2(self):
        # Z = (x - mean) / std
        # axis 0: 행을 따라(아래 방향), 1: 열을 따라(오른쪽 방향)
        mean = np.mean(self.train_input, axis=0)
        std = np.std(self.train_input, axis=0)
        print(f"mean: {mean}, std: {std}")

        # 표준점수로 변환 (numpy의 브로드캐스팅 이용)
        train_scaled = (self.train_input - mean) / std

        # 전처리 데이터로 산점도 그려보기
        # - 전처리 후 x축, y축의 스케일이 동일해짐
        sp = ([25, 150] - mean) / std
        plt.scatter(train_scaled[:, 0], train_scaled[:, 1])
        plt.scatter(sp[0], sp[1], marker="^")
        plt.xlabel("length")
        plt.ylabel("weight")

        # 전처리된 데이터로 모델 훈련 & 평가
        # ** 테스트 세트 역시 전처리 해주어야 함
        test_scaled = (self.test_input - mean) / std
        
        kn = KNeighborsClassifier()
        kn.fit(train_scaled, self.train_target)
        print(kn.score(test_scaled, self.test_target))
        print(kn.predict([sp]))

        # 이웃에 대해 산점도 그려보기
        distances, indexes = kn.kneighbors([sp])
        print(f"distances: {distances}")
        plt.scatter(train_scaled[indexes, 0], train_scaled[indexes, 1], marker="D")
        plt.show()


if __name__ == "__main__":
    kn = KNeighbors_02_2_Ex()
    kn.ex2()