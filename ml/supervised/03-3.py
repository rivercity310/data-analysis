import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sample import Sample

# [ 특성 공학 ]
# - 기존의 특성을 사용해서 새로운 특성을 뽑아내는 작업
# 변환기: 특성을 만들거나 전처리하기 위한 클래스

# hyper parameter: 모델이 학습하는 것이 아닌 사람이 알려줘야 하는 파라미터
# model parameter: 모델이 스스로 학습하는 파라미터

class PolynomialFeatures_03_3_Ex:
    def __init__(self):
        sample = Sample()
        self.perch_full, self.perch_weight = sample.read_remote_perch_data()

        tmp = train_test_split(self.perch_full, self.perch_weight, random_state=42)
        self.train_input = tmp[0]
        self.test_input = tmp[1]
        self.train_target = tmp[2]
        self.test_target = tmp[3]


    def ex1(self):
        # PolynomialFeatures 클래스
        # - 각 특성을 곱한 값, 각 특성을 제곱한 값, 1(절편의 계수)
        # - include_bias=False -> 1(절편의 계수)을 포함하지 않음
        # - 메서드
        #   - fit(): 새롭게 만들 특성 조합을 찾음
        #   - transform(): 실제로 데이터를 변환
        poly = PolynomialFeatures(include_bias=False)
        poly.fit([[2, 3]])
        print(poly.transform([[2, 3]]))
        print(poly.fit_transform([[2, 3]]))     # fit + transform

        del poly

        # 훈련 데이터에 특성 추가해보기
        poly = PolynomialFeatures(include_bias=False)
        poly.fit(self.train_input)

        # ** 훈련 세트를 기준으로 테스트 세트를 변환하는 것이 좋다
        train_poly = poly.transform(self.train_input)
        test_poly = poly.fit_transform(self.test_input)

        print(train_poly.shape)
        print(test_poly.shape)
        print(poly.get_feature_names_out())     # 특성이 어떤 조합으로 만들어쟜는지 확인


    # 추가된 특성들로 다중 회귀 모델 훈련
    def ex2(self):
        poly = PolynomialFeatures()
        poly.fit(self.train_input)
        train_poly = poly.transform(self.train_input)
        test_poly = poly.transform(self.test_input)

        # 사이킷런 모델은 자동으로 특성에 추가된 절편 항을 무시함
        # 따라서 굳이 include_bias=False를 지정할 필요 없음
        lr = LinearRegression()
        lr.fit(train_poly, self.train_target)

        # 결정계수 확인
        print(lr.score(train_poly, self.train_target))
        print(lr.score(test_poly, self.test_target))

        del poly, lr

        # degree 매개변수를 사용하여 최대 차수 지정
        poly = PolynomialFeatures(degree=5)
        poly.fit(self.train_input)
        train_poly = poly.transform(self.train_input)
        test_poly = poly.transform(self.test_input)

        print(train_poly.shape, test_poly.shape)
        print(poly.get_feature_names_out())

        # 다중 회귀 모델 훈련
        lr = LinearRegression()
        lr.fit(train_poly, self.train_target)

        # 결정계수 출력하기
        # - 특성의 개수를 크게 늘리면 훈련 세트에 너무 과대적합 됨
        print(lr.score(train_poly, self.train_target)) 
        print(lr.score(test_poly, self.test_target))               


    # [ 규제 ]
    # - 모델이 훈련 세트를 너무 과도하게 학습하지 못하도록 훼방
    # - 선형 회귀 모델에서는 특성에 곱해지는 계수(기울기)의 크기를 작게 만드는 것
    # - 기울기를 줄이면 보다 보편적인 패턴을 학습한다.
    
    # [ 선형 회귀에 규제를 추가한 대표적인 모델 ]
    # - Ridge: 계수를 제곱한 값을 기준으로 규제 적용
    # - Lasso: 계수의 절댓값을 기준으로 규제 적용    
    def ex3(self):
        # 특성 추가 & 표준 정규화
        train_scaled, test_scaled = self.get_scaled_train_test_split(degree=5)

        # 릿지 회귀
        # - 많은 특성을 사용했음에도 테스트 세트에서도 좋은 성능을 냄
        # - 모델 객체를 만들 때 alpha 매개변수로 규제 강도 조절
        ridge = Ridge()
        ridge.fit(train_scaled, self.train_target)
        print(ridge.score(train_scaled, self.train_target))
        print(ridge.score(test_scaled, self.test_target))

        alpha = self.get_optimized_alpha_value("Ridge", train_scaled, test_scaled)

        # 찾은 alpha 값으로 다시 모델을 훈련
        ridge = Ridge(alpha = alpha)
        ridge.fit(train_scaled, self.train_target)
        print(ridge.score(train_scaled, self.train_target))
        print(ridge.score(test_scaled, self.test_target))

        # 모델 파라미터 값 출력
        print(ridge.coef_)


    def ex4(self):
        # 특성 추가 & 표준화
        train_scaled, test_scaled = self.get_scaled_train_test_split(degree=5)

        # 라쏘 모델 훈련
        # ** 라쏘 모델은 계수 값을 0으로 만들 수도 있다
        lasso = Lasso()
        lasso.fit(train_scaled, self.train_target)
        print(lasso.score(train_scaled, self.train_target))
        print(lasso.score(test_scaled, self.test_target))

        alpha = self.get_optimized_alpha_value("Lasso", train_scaled, test_scaled)

        # 찾은 최적 alpha 값으로 모델 훈련
        lasso = Lasso(alpha = alpha)
        lasso.fit(train_scaled, self.train_target)
        print(lasso.score(train_scaled, self.train_target))
        print(lasso.score(test_scaled, self.test_target))

        # 라쏘 모델의 계수 출력
        print(lasso.coef_)
        print(np.sum(lasso.coef_ == 0))  # 0인 계수의 개수
        
        # 즉, 55개의 특성을 라쏘 모델에 주입했지만 실제 15개 밖에 사용 안함
        # 이러한 라쏘 모델의 특징을 이용하여 유용한 특성을 골라내는 용도로 사용 가능
        print(f"유용한 특성 개수: {len(lasso.coef_) - np.sum(lasso.coef_ == 0)}")


    def get_scaled_train_test_split(self, degree = 2):
        poly = PolynomialFeatures(include_bias = False, degree = degree)
        poly.fit(self.train_input)
        train_poly = poly.transform(self.train_input)
        test_poly = poly.transform(self.test_input)

        ss = StandardScaler()
        ss.fit(train_poly)
        train_scaled = ss.transform(train_poly)
        test_scaled = ss.transform(test_poly)

        return train_scaled, test_scaled
    

    def get_optimized_alpha_value(self, mtype, train_scaled, test_scaled):
        train_scores = []
        test_scores = []
        alpha_list = [0.001, 0.01, 0.1, 1, 10, 100]        

        for alpha in alpha_list:
            model = Ridge(alpha = alpha, max_iter = 10000) if mtype == "Ridge" else Lasso(alpha = alpha, max_iter = 10000) 
            model.fit(train_scaled, self.train_target)
            
            train_score = model.score(train_scaled, self.train_target)
            test_score = model.score(test_scaled, self.test_target)

            train_scores.append(train_score)
            test_scores.append(test_score)

        np_train_scores = np.array(train_scores)
        np_test_scores = np.array(test_scores)
        np_subtract_scores = np_train_scores - np_test_scores

        plt.plot(np.log10(alpha_list), np_train_scores)
        plt.plot(np.log10(alpha_list), np_test_scores)
        # plt.plot(np.log10(alpha_list), np_subtract_scores)
        plt.xlabel("alpha")
        plt.ylabel("R^2")
        plt.show()

        index = np.where(np_subtract_scores == np.min(np_subtract_scores))[0][0]
        return alpha_list[index]


if __name__ == "__main__":
    pf = PolynomialFeatures_03_3_Ex()
    pf.ex4()

