# K-최근접 이웃 회귀
# 지도 학습은 크게 "분류"와 "회귀"로 나뉨
# - 분류: 샘플을 몇 개의 클래스 중 하나로 분류하는 문제
# - 회귀: 샘플을 어떤 임의의 숫자로 예측

# [K-최근접 이웃 분류]: 샘플에 가장 가까운 K개를 골라 다수에 해당하는 클래스로 해당 샘플을 예측
# [K-최근접 이웃 회귀]: 샘플에 가장 가까운 K개의 수치를 평균 내어 값 예측
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_absolute_error


perch_length = np.array([8.4, 13.7, 15.0, 16.2, 17.4, 18.0, 18.7, 19.0, 19.6, 20.0, 21.0,
       21.0, 21.0, 21.3, 22.0, 22.0, 22.0, 22.0, 22.0, 22.5, 22.5, 22.7,
       23.0, 23.5, 24.0, 24.0, 24.6, 25.0, 25.6, 26.5, 27.3, 27.5, 27.5,
       27.5, 28.0, 28.7, 30.0, 32.8, 34.5, 35.0, 36.5, 36.0, 37.0, 37.0,
       39.0, 39.0, 39.0, 40.0, 40.0, 40.0, 40.0, 42.0, 43.0, 43.0, 43.5,
       44.0])

perch_weight = np.array([5.9, 32.0, 40.0, 51.5, 70.0, 100.0, 78.0, 80.0, 85.0, 85.0, 110.0,
       115.0, 125.0, 130.0, 120.0, 120.0, 130.0, 135.0, 110.0, 130.0,
       150.0, 145.0, 150.0, 170.0, 225.0, 145.0, 188.0, 180.0, 197.0,
       218.0, 300.0, 260.0, 265.0, 250.0, 250.0, 300.0, 320.0, 514.0,
       556.0, 840.0, 685.0, 700.0, 700.0, 690.0, 900.0, 650.0, 820.0,
       850.0, 900.0, 1015.0, 820.0, 1100.0, 1000.0, 1100.0, 1000.0,
       1000.0])

train_input, test_input, train_target, test_target = train_test_split(
    perch_length, perch_weight, random_state=42
)
 
# 훈련 세트는 2차원 배열이여야 하므로 shape 변경
train_input = train_input.reshape(-1, 1)
test_input = test_input.reshape(-1, 1)


# 주어진 데이터의 형태를 파악하기 위해 산점도 그려보기
def ex1():
    plt.scatter(perch_length, perch_weight)
    plt.xlabel("length")
    plt.ylabel("weight")
    plt.show()


# Model 훈련
def ex2():
    # KNeighborsRegressor: K-최근접 이웃 회귀 알고리즘 구현 클래스
    knr = KNeighborsRegressor()
    knr.fit(train_input, train_target)

    # 결정계수(R^2) 구하기
    # 값이 높을수록 좋음
    print(knr.score(test_input, test_target))

    # mean_absolute_error
    # 타깃과 예측의 절댓값 오차평균 반환

    # 1. 테스트 세트에 대한 예측 만들기
    test_prediction = knr.predict(test_input)

    # 2. 테스트 세트에 대한 평균 절댓값 오차 계산
    # -> 즉, 예측값이 평균적으로 {mae}값만큼 타깃값과 다르다
    mae = mean_absolute_error(test_target, test_prediction)
    print(mae)


# 과대적합 vs 과소적합
def ex3():
    knr = KNeighborsRegressor()
    knr.fit(train_input, train_target)

    # 훈련 세트와 테스트 세트의 결정계수 비교해보기
    print(knr.score(train_input, train_target))
    print(knr.score(test_input, test_target))

    # 1. 과대적합
    # - 상대적으로 테스트 세트의 결정계수 값이 낮은 경우
    # - 모델이 훈련 세트에 "과대적합"되었음.
    # - 즉, 훈련 세트에만 잘 맞는 모델이라 실전에 대한 예측의 기대가 떨어짐

    # 2. 과소적합
    # - 훈련 세트보다 테스트 세트의 점수가 높거나, 두 점수 모두 낮은 경우
    # - 모델이 훈련 세트에 "과소적합"되었음.
    # - 즉, 모델이 너무 단순하여 적절히 훈련되지 않은 경우

    # [ 과소적합 해결 ]
    # - K값을 줄여 모델을 더 복잡하게 만든다
    # - K값을 늘릴 수록 데이터 전반의 일반적인 패턴을 따르고,
    # - 줄일 수록 데이터의 국지적인 패턴에 민감해진다.

    # 이웃의 개수(K)를 줄이고, 모델을 재훈련 시킨다.
    knr.n_neighbors = 3
    knr.fit(train_input, train_target)
    print(knr.score(train_input, train_target))
    print(knr.score(test_input, test_target))


if __name__ == "__main__":
    ex3()