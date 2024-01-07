import numpy as np
import matplotlib.pyplot as plt
from sample import Sample
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from scipy.special import expit


# [ 로지스틱 회귀 ]


class LogisticRegression_04_1_Ex:
    def __init__(self):
        sample = Sample()
        fish_input, fish_target = sample.read_remote_fish_data()
        tmp = train_test_split(fish_input, fish_target, random_state = 42)

        self.train_input = tmp[0]
        self.test_input = tmp[1]
        self.train_target = tmp[2]
        self.test_target = tmp[3]

        # 훈련 세트, 테스트 세트 표준화 전처리
        ss = StandardScaler()
        ss.fit(self.train_input)
        self.train_scaled = ss.transform(self.train_input)
        self.test_scaled = ss.transform(self.test_input)


    # K-최근접 이웃 분류기의 확률 예측
    def ex1(self):
        # 모델 훈련 & 평가
        kn = KNeighborsClassifier(n_neighbors = 3)
        kn.fit(self.train_scaled, self.train_target)

        print(kn.score(self.train_scaled, self.train_target))
        print(kn.score(self.test_scaled, self.test_target))
        print(kn.classes_)

        # 첫 5개의 샘플에 대한 예측
        print(kn.predict(self.test_scaled[:5]))

        # 클래스별 확률값 출력
        proba = kn.predict_proba(self.test_scaled[:5])
        print(np.round(proba, decimals = 4))

        # 가장 가까운 이웃 정보 출력
        distances, indexes = kn.kneighbors(self.test_scaled[3:4])
        print(self.train_target[indexes])


    def ex2(self):
        # 로지스틱 회귀
        # - 이름은 회귀이지만 분류 모델에 속함
        # - 선형 회귀와 동일하게 선형 방정식 학습
        # - 확률이므로 Sigmoid Function(Logistic Function)을 사용하여 아주 큰 음수일 때 0, 아주 큰 양수일 때 1이 되도록 변경
        # - Sigmoid Function = 1 / (1 + e^(-z)), z는 선형 방정식의 결과값

        # 시그모이드 함수 그려보기
        z = np.arange(-5, 5, 0.1)
        phi = 1 / (1 + np.exp(-z))

        plt.plot(z, phi)
        plt.xlabel("z")
        plt.ylabel("phi")
        plt.show()

    
    # 로지스틱 회귀로 이진 분류하기
    # 0.5 이하인 경우 음성 클래스, 0.5 초과인 경우 양성 클래스로 판단
    def ex3(self):
        # Numpy 불리언 인덱싱
        char_arr = np.array(['A', 'B', 'C', 'D', 'E'])
        print(char_arr[[True, False, True, False, False]])

        # 불리언 인덱싱으로 훈련 세트에서 도미와 빙어만 골라내기
        bream_smelt_indexes = (self.train_target == "Bream") | (self.train_target == "Smelt")
        train_bream_smelt = self.train_scaled[bream_smelt_indexes]
        target_bream_smelt = self.train_target[bream_smelt_indexes]

        # 골라낸 데이터로 로지스틱 회귀 모델 훈련
        lr = LogisticRegression()
        lr.fit(train_bream_smelt, target_bream_smelt)
        print(lr.predict(train_bream_smelt[:5]))
        print(lr.predict_proba(train_bream_smelt[:5]))

        # 로지스틱 회귀 모델이 학습한 계수 출력
        print(f"계수 = {lr.coef_}")
        print(f"절편 = {lr.intercept_}")
        decisions = lr.decision_function(train_bream_smelt[:5])
        print(f"z = {decisions}")

        # 얻은 z값을 시그모이드 함수에 통과시켜 확률 얻기
        print(expit(decisions))


if __name__ == "__main__":
    lr = LogisticRegression_04_1_Ex()
    lr.ex3()