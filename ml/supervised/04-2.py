# [ 점진적 학습 ]
# - partial_fit()
# - epoch: 훈련 세트를 한 번 모두 사용하는 과정

# [ 방식 ]
# 1. 확률적 경사 하강법: 샘플 1개씩 사용
# 2. 미니배치 경사 하강법: 샘플 n개씩 사용
# 3. 배치 경사 하강법: 전체 데이터 사용하기 때문에 컴퓨터 자원을 많이 사용

# [ 손실 함수 ]
# 머신러닝 알고리즘을 측정하는 기준 (값이 작을수록 좋은 알고리즘)
# 연속적인 함수이어야 함 (미분 가능)
# 어떤 값이 최솟값인지 알지 못하기 때문에 가장 작은 값을 찾기 위해서 확률적 경사 하강법 사용 

# [ 손실 함수의 종류 ]
# 1. 로지스틱 손실 함수(이진 크로스엔트로피 손실 함수)
#   - 타깃이 1일 때 -log(k), 타깃이 0일 때 -log(1 - k), k는 예측 확률
#   - 이 손실 함수를 사용하면 "로지스틱 회귀 모델"이 만들어짐
# 2. 크로스엔트로피 손실 함수
#   - 다중 분류에서 사용하는 손실 함수
# 
# ** 회귀의 손실 함수로는 MAE와 MSE가 많이 사용된다. 
# - MAE(Mean Absolute Error, 평균 절댓값 오차): f = sigma(abs(target - predict)) / len(target)
# - MSE(Mean Squared Error, 평균 제곱 오차) : f = sigma(square(target - predict)) / len(target)


import sys
import numpy as np
import matplotlib.pyplot as plt

# 모듈 경로 지정 (동일 폴더 아닌 경우)
sys.path.append(r"C:\Users\seungsu\Desktop\projects\unittest\ml")

from sample import Sample
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import SGDClassifier

class SGDClassifierEx:
    def __init__(self):
        sample = Sample()
        fish_input, fish_target = sample.read_remote_fish_data()

        tmp = train_test_split(fish_input, fish_target, random_state = 42)

        self.train_input = tmp[0]
        self.test_input = tmp[1]
        self.train_target = tmp[2]
        self.test_target = tmp[3]

        ss = StandardScaler()
        ss.fit(self.train_input)
        
        self.train_scaled = ss.transform(self.train_input)
        self.test_scaled = ss.transform(self.test_input)


    def ex1(self):
        # loss: 손실 함수의 종류 지정
        # max_iter: 반복한 에포크 횟수
        sc = SGDClassifier(loss = "log_loss", max_iter = 10, random_state= 42)
        sc.fit(self.train_scaled, self.train_target)

        print(sc.score(self.train_scaled, self.train_target))
        print(sc.score(self.test_scaled, self.test_target))

        # 아직은 에포크 횟수가 부족하여 과소적합
        # partial_fit() 메서드로 점진적 학습 시키기 
        sc.partial_fit(self.train_scaled, self.train_target)
        print(sc.score(self.train_scaled, self.train_target))
        print(sc.score(self.test_scaled, self.test_target))


    # 에포크에 따른 정확도 그래프 그려보기
    def ex2(self):
        sc = SGDClassifier(loss = "log_loss", random_state = 42)

        train_score = []
        test_score = []
        classes = np.unique(self.train_target)

        # 300번의 에포크동안 반복
        # partial_fit() 메서드만 사용하여 훈련하려면 훈련 세트의 전체 클래스 레이블을 전달해주어야 함
        for _ in range(300):
            sc.partial_fit(self.train_scaled, self.train_target, classes = classes) 
            train_score.append(sc.score(self.train_scaled, self.train_target))
            test_score.append(sc.score(self.test_scaled, self.test_target))
 
        # 그래프 그리기
        plt.plot(train_score)
        plt.plot(test_score)
        plt.xlabel("epoch")
        plt.ylabel("accuracy")
        plt.show()

        # 찾은 최적의 에포크 횟수(100)로 모델 다시 훈련
        # tol: 일정 에포크 동안 성능이 향상되지 않으면 더 훈련하지 않고 자동으로 멈춤
        sc = SGDClassifier(loss = "log_loss", max_iter = 100, tol = None, random_state = 42)
        sc.fit(self.train_scaled, self.train_target)
        print(sc.score(self.train_scaled, self.train_target))
        print(sc.score(self.test_scaled, self.test_target))


if __name__ == "__main__":
    sgd = SGDClassifierEx()
    sgd.ex2()
