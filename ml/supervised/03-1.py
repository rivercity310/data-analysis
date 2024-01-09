import matplotlib.pyplot as plt
from sample import Sample
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_absolute_error

# K-최근접 이웃 회귀
# 지도 학습은 크게 "분류"와 "회귀"로 나뉨
# - 분류: 샘플을 몇 개의 클래스 중 하나로 분류하는 문제
# - 회귀: 샘플을 어떤 임의의 숫자로 예측
# [K-최근접 이웃 분류]: 샘플에 가장 가까운 K개를 골라 다수에 해당하는 클래스로 해당 샘플을 예측
# [K-최근접 이웃 회귀]: 샘플에 가장 가까운 K개의 수치를 평균 내어 값 예측 
class KNeighbors_03_1_Ex:
    def __init__(self):
        sample = Sample()
        self.train_input, self.test_input, self.train_target, self.test_target = sample.get_sample_data()
        self.perch_length, self.perch_weight = sample.get_perch_data()


    # 주어진 데이터의 형태를 파악하기 위해 산점도 그려보기
    def ex1(self):
        plt.scatter(self.perch_length, self.perch_weight)
        plt.xlabel("length")
        plt.ylabel("weight")
        plt.show()


    # Model 훈련
    def ex2(self):
        # KNeighborsRegressor: K-최근접 이웃 회귀 알고리즘 구현 클래스
        knr = KNeighborsRegressor()
        knr.fit(self.train_input, self.train_target)

        # 결정계수(R^2) 구하기
        # 값이 높을수록 좋음
        print(knr.score(self.test_input, self.test_target))

        # MAE(mean_absolute_error, 평균절대오차)
        # - 타깃과 예측의 절댓값 오차평균 반환
        # - 손실함수 E = sigma(abs(yi - y2i))
        #   - yi = i번째 학습 데이터의 정답, y2i = i번째 학습 데이터로 예측한 값 

        # 1. 테스트 세트에 대한 예측 만들기
        test_prediction = knr.predict(self.test_input)
        print(f"test_target: {self.test_target}")
        print(f"test_prediction: {test_prediction}")

        abs_sum = 0

        for target_score, predict_score in zip(self.test_target, test_prediction):
            abs_sum += abs(target_score - predict_score)
            
        # 2. 테스트 세트에 대한 평균 절댓값 오차 계산
        # -> 즉, 예측값이 평균적으로 {mae}값만큼 타깃값과 다르다
        mae = mean_absolute_error(self.test_target, test_prediction)
        print(f"MAE: {mae}")
        print(f"abs_sum: {abs_sum / len(self.test_target)}")
        print(mae == abs_sum / len(self.test_target))        # True


    # 과대적합 vs 과소적합
    def ex3(self):
        knr = KNeighborsRegressor()
        knr.fit(self.train_input, self.train_target)

        # 훈련 세트와 테스트 세트의 결정계수 비교해보기
        print(knr.score(self.train_input, self.train_target))
        print(knr.score(self.test_input, self.test_target))

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
        knr.fit(self.train_input, self.train_target)
        print(knr.score(self.train_input, self.train_target))
        print(knr.score(self.test_input, self.test_target))    


if __name__ == "__main__":
    kn = KNeighbors_03_1_Ex()
    kn.ex3()