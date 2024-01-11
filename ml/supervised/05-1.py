import sys
import matplotlib.pyplot as plt
import numpy as np

sys.path.append(r"C:\Users\seungsu\Desktop\projects\unittest\ml")

from sample import Sample
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import plot_tree


# 결정 트리
class DecisionTreeEx:
    def __init__(self):
        sample = Sample()
        wine_data, wine_target = sample.read_remote_wine_data()
        tmp = train_test_split(wine_data, wine_target, test_size = 0.2)

        self.train_input = tmp[0]
        self.test_input = tmp[1]
        self.train_target = tmp[2]
        self.test_target = tmp[3]

    
    # 로지스틱 회귀로 와인 종류 분류해보기
    def ex1(self):
        # 데이터 표준화 전처리 (z값으로 변환)
        ss = StandardScaler()
        ss.fit(self.train_input)
        
        train_scaled = ss.transform(self.train_input)
        test_scaled = ss.transform(self.test_input)

        # 표준화된 데이터로 로지스틱 회귀 모델 훈련
        lr = LogisticRegression()
        lr.fit(train_scaled, self.train_target)

        # 모델 과소적합 (규제 매개변수 C 설정?, solver 매개변수에 다른 알고리즘?)
        print(lr.score(train_scaled, self.train_target))
        print(lr.score(test_scaled, self.test_target))

        # 로지스틱 회귀 모델이 학습한 계수와 절편 등을 출력
        print(lr.classes_)
        print(lr.coef_, lr.intercept_)
        print(lr.decision_function(train_scaled))   # z값 출력
        print(lr.predict_proba(train_scaled))       # 시그모이드 함수 통과

        # z값을 시그모이드 함수 통과시키기
        decisions = lr.decision_function(train_scaled)
        sigmoids = list()

        for decision in decisions:
            sigmoid = 1 / (1 + np.exp(-decision))    
            sigmoids.append(sigmoid)
        
        # 그래프 그려보기
        plt.scatter(np.arange(0, len(train_scaled)), sigmoids)    
        plt.xlabel("index")
        plt.ylabel("sigmoid")
        plt.show()


    # 결정 트리
    # - 각 노드의 질문에 따라 트리를 이동, 마지막에 도달한 노드의 클래스 비율을 통해 예측을 만듬 
    def ex2(self):
        # 데이터 표준화 전처리
        ss = StandardScaler()
        ss.fit(self.train_input)
        
        train_scaled = ss.transform(self.train_input)
        test_scaled = ss.transform(self.test_input)

        # 결정 트리 모델 훈련 (과대 적합)
        dt = DecisionTreeClassifier(criterion = 'entropy') # default 'gini'
        dt.fit(train_scaled, self.train_target)
        
        print(dt.score(train_scaled, self.train_target))
        print(dt.score(test_scaled, self.test_target))

        # 결정 트리 그림 출력해보기
        plt.figure(figsize = (10, 7))
        plot_tree(dt, max_depth = 1, filled = True,
                  feature_names = ['alcohol', 'sugar', 'pH'])
        plt.show()

    
    # 불순도(impurity)
    # - gini impurity
    #   - DecisionTreeClassifier 클래스의 criterion 매개변수의 기본값이 'gini'
    #   - 지니 불순도 = 1 - (1번 클래스 비율^2 + n번 클래스 비율^2) 
    #   - 어떤 노드의 두 클래스의 비율이 정확히 1/2씩이라면 지니 불순도가 0.5가 되어 최악
    #   - 어떤 노드에 하나의 클래스만 있다면 지니 불순도는 0이 되어 가장 작음 (순수 노드라 함)
    # - entropy impurity
    #   - 지니 불순도에서 제곱을 사용한 것과 달리 밑이 2인 로그 사용
    #   - 1 - (음성 클래스 비율) x log2(음성 클래스 비율) - (양성 클래스 비율) x log2(양성 클래스 비율)
        
    # [ 정보이득 ]
    # 결정 트리 모델은 부모 노드와 자식 노드의 불순도 차이(정보이득)가 가능한 크도록 트리를 성장시킴
    # 노드를 순수하게 나눌 수록 정보이득이 커진다.
    #   - 자식 노드들의 불순도를 샘플 계수에 비례하여 모두 더한 다음, 부모 노드의 불순도에서 뺌
    #   - 정보이득 = 부모의 불순도 - (왼쪽 노드 샘플 수 / 부모 노드 샘플 수) x 왼쪽 노드 불순도 - (오른쪽 노드 샘플 수 ......) ..
    
    # [ 가지치기 ]
    # - 가지치기를 하지 않으면 무작정 자라나는 트리 -> 훈련 세트에 과대 적합 (일반화가 안됨)
    # - 가장 간단한 가지치기 방법은 max_depth 매개변수를 지정하는 것 (최대 자라날 깊이 지정)
    def ex3(self):
        # 데이터 표준화 전처리
        ss = StandardScaler()
        ss.fit(self.train_input)

        train_scaled = ss.transform(self.train_input)
        test_scaled = ss.transform(self.test_input)

        # 가지치기 수행
        dt = DecisionTreeClassifier(max_depth = 3)
        dt.fit(train_scaled, self.train_target)

        print(dt.score(train_scaled, self.train_target)) 
        print(dt.score(test_scaled, self.test_target)) 

        # 가지치기된 트리 그래프 그려보기
        plt.figure(figsize = (20, 15))
        plot_tree(dt, filled = True, feature_names = ['alcohol', 'sugar', 'pH'])
        plt.show()

        # 결정 트리의 특성 중요도 출력하기
        print(dt.feature_importances_)


    def ex4(self):
        # [특성을 추가한 뒤 다시 훈련시켜보기]
        poly = PolynomialFeatures(degree = 2, include_bias = False)
        poly.fit(self.train_input, self.train_target)

        train_poly = poly.transform(self.train_input)
        test_poly = poly.transform(self.test_input)

        ss = StandardScaler()
        ss.fit(train_poly, self.train_target)

        train_scaled = ss.transform(train_poly)
        test_scaled = ss.transform(test_poly)

        dt = DecisionTreeClassifier(max_depth = 3)
        dt.fit(train_scaled, self.train_target)

        print(dt.score(train_scaled, self.train_target))
        print(dt.score(test_scaled, self.test_target))

        # 특성 추가된 결정 트리 그래프 그려보기
        plt.figure(figsize = (20, 15))
        plot_tree(dt, filled = True)
        plt.show()
        
        # 특성 중요도 출력
        print(dt.feature_importances_)
        

if __name__ == "__main__":
    dt = DecisionTreeEx()
    dt.ex4()