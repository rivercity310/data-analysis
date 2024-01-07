import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression
from sample import Sample


class LinearRegression_03_2_Ex:
    def __init__(self):
        sample = Sample()
        self.train_input, self.test_input, self.train_target, self.test_target = sample.get_sample_data()


    # K-Neighbors 모델의 문제점: 훈련 범위를 벗어난 데이터를 제대로 처리하지 못함
    # 해당 문제를 해결하기 위해 선형 회귀 모델 사용
    def ex1(self):
        knr = KNeighborsRegressor()
        knr.fit(self.train_input, self.train_target)

        # 길이가 훈련 범위를 넘어선 농어 무게 예측
        # 두 값이 모두 동일한 값으로 예측되는 문제점
        print(knr.predict([[50]]))  
        print(knr.predict([[70]]))

        # kneighbors(): 가장 가까운 이웃까지의 거리와 샘플의 인덱스 구하기
        _distances, indexes = knr.kneighbors([[50]]) # 50cm 농어의 이웃 구하기

        plt.scatter(self.train_input, self.train_target)
        plt.scatter(self.train_input[indexes], self.train_target[indexes], marker='D')
        plt.scatter(50, 1010, marker="^")
        
        plt.xlabel("length")
        plt.ylabel("weight")
        plt.show()


    # 선형 회귀: 특성이 하나인 경우 어떤 직선을 학습하는 알고리즘
    # 즉, 직선의 방정식 y=ax+b에서 훈련을 통해 적절한 a와 b를 찾아낸다.
    def ex2(self):
        lr = LinearRegression()
        lr.fit(self.train_input, self.train_target)
        print(lr.predict([[50]]))

        # 모델 파라미터: 머신러닝 알고리즘이 찾은 값 (모델 기반 학습) <-> 사례 기반 학습
        # coef_: 기울기, intercept_: 절편
        print(lr.coef_, lr.intercept_)

        # [ 직선의 방정식 그리기 ]
        # 1. 훈련 세트의 산점도 그리기 
        plt.scatter(self.train_input, self.train_target)

        # 2. 찾은 모델 파라미터를 이용하여 두 점을 이은 직선의 방정식 그리기
        plt.plot([15, 50], [15 * lr.coef_ + lr.intercept_, 50 * lr.coef_ + lr.intercept_])
        
        # 3. 50cm 농어 데이터 표시하기
        plt.scatter(50, 1241.8, marker="^")
        plt.xlabel("length")
        plt.ylabel("weight")
        plt.show()

        # [ 결정 계수 값 확인해보기 ] 
        # - 훈련 세트의 값이 테스트 세트의 값보다 많이 큼 -> 과대적합?
        # - 하지만 훈련 세트의 값도 절대적으로 높지 않음
        # - 따라서 전체적으로 과소적합 되었다고 볼 수 있음.
        print(lr.score(self.train_input, self.train_target))
        print(lr.score(self.test_input, self.test_target))


    # 선형 회귀의 과소적합 문제 해결
    # - 1. 무게가 0 이하인 농어는 없다
    # - 2. 데이터의 분포는 직선보다는 곡선에 가깝다.
    # -> 따라서 2차 방정식 형태의 다항 회귀를 사용한다. 
    def ex3(self):
        # 2차 방정식의 그래프를 그리기 위해 길이를 제곱한 항을 훈련 세트 첫번째에 추가
        # np.column_stack을 이용하면 쉽게 컬럼 추가 가능 (넘파이 브로드캐스팅)
        train_poly = np.column_stack((self.train_input ** 2, self.train_input))
        test_poly = np.column_stack((self.test_input ** 2, self.test_input))

        lr = LinearRegression()
        lr.fit(train_poly, self.train_target)

        print(lr.predict([[50 ** 2, 50]]))    # 50cm 데이터에 대한 예측값 출력
        print(lr.coef_, lr.intercept_)        # 기울기값과 절편 출력

        # 산점도와 그래프 그리기
        # 2차 방정식(곡선)은 짧은 직선을 이어서 그려 표현한다
        point = np.arange(15, 51)
        
        plt.scatter(self.train_input, self.train_target)
        plt.plot(point, lr.coef_[0] * point ** 2 + lr.coef_[1] * point + lr.intercept_)

        # 50cm 농어 데이터 표시하기
        plt.scatter(50, 1574, marker="^")
        plt.xlabel("length")
        plt.ylabel("weight")
        plt.show()

        # 다시 한번 결정 계수 출력하기 (여전히 과소적합 문제가 발생)
        print(lr.score(train_poly, self.train_target))
        print(lr.score(test_poly, self.test_target))


    def ex4(self):
        pass


if __name__ == "__main__":
    lr = LinearRegression_03_2_Ex()
    lr.ex3()