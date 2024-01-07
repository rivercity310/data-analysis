# [ 머신러닝 알고리즘 종류 ]

# 1. 지도 학습(Supervised Learning)
#   - 입력(데이터)과 타깃(정답)으로 이루어진 훈련 데이터
#   - 입력으로 사용된 각 특성(길이, 무게 등)이 존재
#   - 정답(타깃)이 있으므로 알고리즘이 정답을 맞히는 것을 학습

# 2. 비지도 학습(Unsupervised Learning)
#   - 타깃 없이 입력 데이터만 사용
#   - 정답(타깃)을 사용하지 않으므로 무언가를 맞히는 것이 아닌, 데이터를 변형하거나 파악

# 3. 강화 학습(Reinforcement Learning)
#   - 타깃이 아닌 알고리즘이 행동한 결과로 얻은 보상을 사용해 학습

# ---------------------------------------------------------------------------

# [ 훈련 세트와 테스트 세트 ]

# 머신러닝의 정확한 평가를 위해서는 테스트 세트와 훈련 세트가 따로 준비되어야 한다.
# 즉, 이미 준비된 데이터 중에 일부를 떼어 내어 테스트 세트를 만든다.
#   - 훈련 세트: 훈련에 사용되는 데이터
#   - 테스트 세트: 평가에 사용되는 데이터


import numpy as np
import matplotlib.pyplot as plt
from sample import Sample
from sklearn.neighbors import KNeighborsClassifier


class KNeighbors_02_1_Ex:
    def __init__(self):
        sample = Sample()
        self.fish_length, self.fish_weight = sample.get_fish_data()
        
        # 추후 numpy의 column_stack(), concatenate(), ones(), zeros()로 대체
        self.fish_data = [[l, w] for l, w in zip(self.fish_length, self.fish_weight)]
        self.fish_target = [1] * 35 + [0] * 14
    

    # 샘플링 편향 문제 발생 
    def ex1(self):
        kn = KNeighborsClassifier()

        # 훈련 데이터
        train_input = self.fish_data[:35]
        train_target = self.fish_target[:35]

        # 테스트 데이터
        test_input = self.fish_data[35:]
        test_target = self.fish_target[35:]

        kn.fit(train_input, train_target)
        print(kn.score(test_input, test_target))   # 0.0


    # 무작위로 섞인 인덱스를 통해 샘플 섞기
    # 추후 train_test_split()으로 대체
    def ex2(self):
        np.random.seed(42)  # 랜덤 시드 설정
        index = np.arange(len(self.fish_length))
        np.random.shuffle(index)

        # numpy 배열로 변경
        np_fish_data = np.array(self.fish_data)
        np_fish_target = np.array(self.fish_target)

        # 훈련 세트와 테스트 세트 무작위로 나누기
        # numpy의 배열 인덱싱 기능 -> 여러 인덱스로 한번에 여러 원소 선택
        train_input = np_fish_data[index[:35]]
        train_target = np_fish_target[index[:35]]
        test_input = np_fish_data[index[35:]]
        test_target = np_fish_target[index[35:]]

        # 모델 훈련 & 평가
        kn = KNeighborsClassifier()
        kn.fit(train_input, train_target)
        print(kn.score(test_input, test_target))
        
        # 예측 결과와 실제 타깃 확인해보기
        print(kn.predict(test_input))
        print(test_target)

        # 샘플이 골고루 섞였는지 확인하기 위해 산점도 그리기
        plt.scatter(train_input[:, 0], train_input[:, 1])
        plt.scatter(test_input[:, 0], test_input[:, 1])
        plt.xlabel("length")
        plt.ylabel("weight")
        plt.show()
         

if __name__ == "__main__":
    kn = KNeighbors_02_1_Ex()
    kn.ex2()